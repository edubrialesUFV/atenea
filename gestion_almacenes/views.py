from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from gestion_almacenes import models
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Producto
from .models import Proveedor
# Create your views here.
from .forms import FiltroProveedorForm, ClienteCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from .forms import FiltroProveedorForm
from django.urls import reverse
from .models import Producto, Pedido, Cliente
from django.utils import timezone
from gestion_almacenes.models import Pedido, PedidoProducto, ProductoPosicion
from .models import Pedido, PedidoProducto
from .forms import PedidoFilterForm

from .forms import FiltroProveedorForm
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
            messages.error(request, f'Sólo hay {producto.cantidad_stock} unidades disponibles')
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
        precio = producto.id
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
        productos = []
        total = 0
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
        
        cliente = Cliente.objects.get(id=request.user.id)

        pedido = Pedido.objects.create(
            cliente=cliente,
            fecha_hora_pedido=timezone.now(),
            tipo_envio=tipo_envio,
            agencia_transporte=agencia_transporte,
        )
        
        messages.success(request, 'La compra se ha procesado correctamente.')
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

