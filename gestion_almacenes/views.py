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

from django.shortcuts import render
from .models import Producto
import pandas as pd

def mostrar_productos(request):
    # Ruta relativa al archivo Excel desde el directorio raíz del proyecto
    ruta_excel = 'Proov_Ref_2023-1.xlsx'

    # Leer el archivo Excel utilizando pandas
    dataframe = pd.read_excel(ruta_excel)

    # Obtener los datos necesarios del dataframe
    productos = dataframe['Producto'].tolist()
    caracteristicas = dataframe['Caracteristicas'].tolist()

    # Renderizar una respuesta en el navegador con los datos obtenidos
    return render(request, 'mostrar_productos.html', {'productos': productos, 'caracteristicas': caracteristicas})

