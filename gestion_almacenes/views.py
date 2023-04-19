from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from gestion_almacenes import models
from django.shortcuts import render
from .models import Producto
from .models import Proveedor
# Create your views here.

from .forms import FiltroProveedorForm
from django.db.models import Q

from .forms import FiltroProveedorForm

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




