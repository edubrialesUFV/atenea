from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from gestion_almacenes import models
from django.shortcuts import render
from .models import Producto
# Create your views here.

def index(request):
    productos = Producto.objects.all()
    return render(request, "index.html", {'productos': productos})


@staff_member_required
def registrar_producto(request):
    return render(request, "registrar_producto.html")


def producto_detail(request, id):
    producto = get_object_or_404(models.Producto, referencia=id)
    return render(request, "product_detail.html", {'producto': producto}) 




