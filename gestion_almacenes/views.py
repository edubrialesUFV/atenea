from django.shortcuts import render 
from django.contrib.admin.views.decorators import staff_member_required
# Create your views here.

def index(request):
    return render(request, "index.html")


@staff_member_required
def registrar_producto(request):
    return render(request, "registrar_producto.html")
