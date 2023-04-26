from io import BytesIO
import re
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from django.urls import reverse
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import get_template

from gestion_almacenes import models
from gestion_almacenes.models import Pedido, PedidoProducto, ProductoPosicion

from .models import Producto, Pedido, Cliente
from .models import Producto, Posicion
from .models import Proveedor
from .models import Pedido, PedidoProducto

from .forms import FiltroProveedorForm, ClienteCreationForm
from .forms import FiltroProveedorForm
from .forms import PedidoFilterForm
from .forms import FiltroProveedorForm

from .utils import pedir_proveedores, migrations_picstock, product_type
from xhtml2pdf import pisa

from datetime import timedelta
from django.utils import timezone

class ClienteLoginView(LoginView):
    template_name = 'login.html'
    def get_success_url(self):
        return reverse('home')


def register(request):
    if request.method == 'POST':
        form = ClienteCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = ClienteCreationForm()
    return render(request, 'register.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')

def index(request):
    # Obtener los proveedores directamente de los objetos Producto
    proveedores = Proveedor.objects.values_list('nombre_proveedor', flat=True).distinct()

    form = FiltroProveedorForm(proveedores)
    productos = Producto.objects.all()

    if request.method == 'POST':
        form = FiltroProveedorForm(proveedores, request.POST)
        if form.is_valid():
            proveedor_seleccionado = form.cleaned_data['proveedor']
            if proveedor_seleccionado:
                productos = productos.filter(proveedor__nombre_proveedor=proveedor_seleccionado)

    productos_modificados = []

    for producto in productos:
        referencia_modificada = producto.referencia.split('_')[0].capitalize()

        if referencia_modificada == 'Pinta':
            referencia_modificada = 'Pintalabios'

        if referencia_modificada == 'Locion':
            referencia_modificada = 'Loción'

        if referencia_modificada == 'Cosmetico':
            referencia_modificada = 'Cosmético'

        producto_dict = {
            'referencia': producto.referencia,
            'referencia_mod': referencia_modificada,
            'proveedor': producto.proveedor,
            'cantidad_stock': producto.cantidad_stock,
            'peso_por_unidad': producto.peso_por_unidad,
        }
        productos_modificados.append(producto_dict)

    return render(request, 'index.html', {'productos': productos_modificados, 'form': form})


@staff_member_required
def registrar_producto(request):
    if request.method == 'POST':
        codigo = request.POST.get('codigo')
        print(codigo)
        
        pattern = r'^([A-Za-z]+)(\d+)-(\d+)-([A-Za-z]+)$'

        match = re.match(pattern, codigo)
        if match:
            type_code, number, quantity, supplier = match.groups()
            full_product_name = f'{product_type(type_code)}_{number}'
            print(f'Nombre completo del producto: {full_product_name}')
            print(f'Cantidad del producto: {quantity}')
            print(f'Proveedor del producto: {supplier}')
            quantity = int(quantity)
            nuevo_producto = Producto.objects.get(referencia = full_product_name)
            nuevo_producto.cantidad_stock = nuevo_producto.cantidad_stock + quantity
            nuevo_producto.save()
            posiciones = ProductoPosicion.objects.filter(producto = nuevo_producto).order_by("posicion")
            posicion_picking = Posicion.objects.get(id = posiciones[0].posicion.id)
            posicion_stock = Posicion.objects.get(id = posiciones[1].posicion.id)
            if posicion_picking.unidades_ocupadas < 20:
                cantidad_restante = 20 - posicion_picking.unidades_ocupadas
                posicion_picking.unidades_ocupadas = posicion_picking.unidades_ocupadas + cantidad_restante
                cantidad_restante = quantity - cantidad_restante
                posicion_stock.unidades_ocupadas = posicion_stock.unidades_ocupadas + cantidad_restante
                posicion_picking.save()
                posicion_stock.save()
                messages.success(request, f'Se han añadido {quantity} unidades de {full_product_name} al sistema')
                return redirect('/admin')
            else:
                posicion_stock.unidades_ocupadas = posicion_stock.unidades_ocupadas + quantity
                posicion_stock.save()
                messages.success(request, f'Se han añadido {quantity} unidades de {full_product_name} al sistema')
                return redirect('/admin')
        else:
            print('El código proporcionado no coincide con el patrón esperado.')
            messages.error(request, f'El codigo proporcionado no sigue el formato patron esperado')
    return render(request, "registrar_producto.html")


def producto_detail(request, id):
    producto = get_object_or_404(models.Producto, referencia=id)
    nombre_referencia = producto.referencia.split('_')[0].capitalize()
    return render(request, "product_detail.html", {'producto': producto, 'nombre': nombre_referencia})

def anadirAcesta(request, id):
    producto = get_object_or_404(models.Producto, referencia=id)
    referencia = producto.referencia
    nombre_referencia = producto.referencia.split('_')[0].capitalize()
    
    if request.method == 'POST':
        cantidad = int(request.POST.get('cantidad', 0))
        
        if cantidad > producto.cantidad_stock:
            return redirect(f'/product_detail/{producto.id}/')  # Redirige al usuario a la página de detalle del producto
        else:
            carrito = request.session.get('carrito', {})
            carrito[producto.id] = {'referencia': referencia, 'cantidad': cantidad}
            request.session['carrito'] = carrito
            messages.success(request, f'{cantidad} unidades de {nombre_referencia} han sido añadidas al carrito')
            return redirect('/checkout/')
    else:
        messages.error(request, f'Sólo hay {producto.cantidad_stock} unidades disponibles')
        return render(request, "product_detail.html", {'producto': producto, 'nombre': nombre_referencia})



def checkout(request):
    carrito = request.session.get('carrito', {})
    productos = []
    total = 0
    for id, item in carrito.items():
        producto = get_object_or_404(models.Producto, id=id)
        precio = producto.precio
        subtotal = precio * item['cantidad']
        total += subtotal
        productos.append({
            'id': producto.id,
            'nombre': producto.referencia,
            'producto': producto,
            'cantidad': item['cantidad'],
            'precio': precio,
            'subtotal': subtotal,
        })

    context = {
        'productos': productos,
        'total': total,
    }
    return render(request, 'checkout.html', context)


from django.contrib.auth.decorators import login_required

@login_required
def procesar_compra(request):
    if request.method == 'POST':
        carrito = request.session.get('carrito', {})
        unidadesTotales = 0
        pesoTotal = 0
        productos = []
        total = 0
        entrega = ''
        for id, item in carrito.items():
            try:
                producto = Producto.objects.get(id=id)
                if producto.cantidad_stock < item['cantidad']:
                    messages.error(request, f"No hay suficientes unidades en stock para el producto '{producto.referencia}'.")
                    return redirect('/checkout/')
                productos.append({
                    'producto': producto,
                    'cantidad': item['cantidad'],
                })
                producto.cantidad_stock -= item['cantidad']
                producto.save()
            except Producto.DoesNotExist:
                raise ValueError(f"No se encontró el producto con ID '{id}'.")
        
        tipo_envio = request.POST.get('tipo_envio')
        agencia_transporte = request.POST.get('agencia_transporte')
        print(tipo_envio)
        cliente = Cliente.objects.get(id=request.user.id)

        pedido = Pedido.objects.create(
            cliente=cliente,
            fecha_hora_pedido=timezone.now(),
            tipo_envio=tipo_envio,
            agencia_transporte=agencia_transporte,
        )

        print(pedido.id)
        for id, item in carrito.items():
            producto = Producto.objects.get(id=id)
            cantidad = item['cantidad']
            unidadesTotales = unidadesTotales + cantidad
            
            pedidoproducto = PedidoProducto.objects.create(
                pedido = pedido,
                producto = producto,
                cantidad = cantidad,
            )
           
        print(pedido.agencia_transporte)
        
        cliente = request.user
        
       # Genera el PDF y guárdalo en el servidor
        output_dir = os.path.join(settings.MEDIA_ROOT, 'etiquetas')
        os.makedirs(output_dir, exist_ok=True)
        filename = f"Comprobante_{cliente.nombre_cliente}_{timezone.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
        output_path = os.path.join(output_dir, filename)

        if pedido.agencia_transporte == "DHL":
            pdf = generar_pdf('comprobanteDHL.html', {'cliente': cliente, 'pedido': pedido, 'productos': productos }, output_path)
        
        elif pedido.agencia_transporte == "COR":
            pesoTotal = unidadesTotales*0.2
            pdf = generar_pdf('comprobanteCorreos.html', {'cliente': cliente, 'pedido': pedido, 'productos': productos , 'carrito': carrito, 'unidadesTotales': unidadesTotales, 'pesoTotal': pesoTotal}, output_path)

        elif pedido.agencia_transporte == "SEU":
            if tipo_envio == "EST":
                now = timezone.now()
                entrega = now + timedelta(days=3)
            elif tipo_envio == "URG":
                now = timezone.now()
                entrega = now + timedelta(days=3)
            
            pesoTotal = unidadesTotales*0.2
            pdf = generar_pdf('comprobanteSeur.html', {'cliente': cliente, 'pedido': pedido, 'productos': productos , 'carrito': carrito, 'unidadesTotales': unidadesTotales, 'pesoTotal': pesoTotal, 'entrega':entrega}, output_path)
        

        if pdf:
            # Opcional: guarda la ruta del archivo en el modelo Pedido
            # pedido = pedido.objects.get( ... ) # Elimina esta línea
            pedido.comprobante = output_path
            pedido.save()

        output_dir = os.path.join(settings.MEDIA_ROOT, 'albaranes')
        filename = f"Albaran_{cliente.nombre_cliente}_{timezone.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
        output_path = os.path.join(output_dir, filename)

        cliente = Cliente.objects.get(id=request.user.id)
        productos = []
        for id, item in carrito.items():
            try:
                producto = Producto.objects.get(id=id)
                productos.append({
                    'producto': producto,
                    'cantidad': item['cantidad'],
                })
            except Producto.DoesNotExist:
                raise ValueError(f"No se encontró el producto con ID '{id}'.")
                
        context = {
            'cliente': cliente,
            'productos': productos,
        }

        pdf = generar_albaran('albaran.html', context, output_path)



        messages.success(request, 'La compra se ha procesado correctamente.')

        request.session['carrito'] = {}
        request.session.save()
        migrations_picstock(productos)
        pedir_proveedores(productos)
        return redirect('/')
    else:
        return redirect('/checkout')

from django.views.decorators.http import require_POST

@require_POST
def eliminar_producto(request, producto_id):
    carrito = request.session.get('carrito', {})
    producto_id = str(producto_id)
    if producto_id in carrito:
        del carrito[producto_id]
        request.session['carrito'] = carrito
    return redirect('/checkout/')


def pedidos_productos(request):
    if request.method == 'POST':
        form = PedidoFilterForm(request.POST)
        if form.is_valid():
            pedido = form.cleaned_data.get('pedido')
            if pedido:
                pedidos = Pedido.objects.filter(id=pedido.id)
            else:
                pedidos = Pedido.objects.all()
        else:
            pedidos = Pedido.objects.all()
    else:
        form = PedidoFilterForm()
        pedidos = Pedido.objects.all()

    pedidos_productos_list = []
    for pedido in pedidos:
        productos = PedidoProducto.objects.filter(pedido=pedido)
        pedidos_productos_list.append({'pedido': pedido, 'productos': productos})

    context = {'pedidos_productos_list': pedidos_productos_list, 'form': form}
    return render(request, 'pedidos_productos.html', context)


import os

def generar_albaran(template_src, context_dict={}, output_filename=None):
    productos = context_dict.get('productos', [])  # Obtén la lista de productos del contexto
    
    total = 0  # Inicializa el total en 0
    
    # Calcula el subtotal de cada producto y suma al total
    for producto in productos:
        precio = producto['producto'].precio
        cantidad = producto['cantidad']
        subtotal = precio * cantidad
        producto['subtotal'] = subtotal  # Agrega el subtotal al producto en el contexto
        total += subtotal
    
    context_dict['total'] = total

    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        if output_filename:
            with open(output_filename, "wb") as f:
                f.write(result.getvalue())
        return result.getvalue()
    else:
        return None

def generar_pdf(template_src, context_dict={}, output_filename=None):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        if output_filename:
            with open(output_filename, "wb") as f:
                f.write(result.getvalue())
        return result.getvalue()
    else:
        return None

