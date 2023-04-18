from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from gestion_almacenes import models
# Create your views here.

def index(request):
    return render(request, "index.html")


@staff_member_required
def registrar_producto(request):
    return render(request, "registrar_producto.html")


def producto_detail(request, id):
    producto = get_object_or_404(models.Producto, referencia=id)
    return render(request, "product_detail.html", {'producto': producto}) 

    