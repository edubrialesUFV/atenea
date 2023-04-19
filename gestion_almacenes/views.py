from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from gestion_almacenes import models
from django.shortcuts import render, redirect
from .models import Producto
from .models import Proveedor
# Create your views here.
from .forms import FiltroProveedorForm, ClienteCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login, logout
from .forms import FiltroProveedorForm
from django.urls import reverse

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
    return render(request, "registrar_producto.html")


def producto_detail(request, id):
    producto = get_object_or_404(models.Producto, referencia=id)
    nombre_referencia = producto.referencia.split('_')[0].capitalize()
    return render(request, "product_detail.html", {'producto': producto, 'nombre_referencia': nombre_referencia}) 




