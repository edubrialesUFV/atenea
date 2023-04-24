import os
import sys
import django
import openpyxl
from django.core.exceptions import ValidationError
import random
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atenea.settings")
django.setup()

from gestion_almacenes.models import Proveedor, Producto, Posicion, ProductoPosicion

def cargar_datos(archivo_xlsx):
    wb = openpyxl.load_workbook(archivo_xlsx)
    hoja = wb['Hoja1']
    i=0
          
    # Asumiendo que la primera fila tiene encabezados y los datos comienzan en la segunda fila
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        posicionesPicking = Posicion(id ="P"+str(i), tipo_posicion="PIC", capacidad=20, unidades_ocupadas=20 )     
        posicionesStock = Posicion(id="S"+str(i), tipo_posicion="STO", capacidad=20 )
        posicionesPicking.save()
        posicionesStock.save() 
        prov, ref, cant_min = fila
        ref_mod = ref.lower()
        ref_mod = ref_mod.replace(" ", "_")
        ref_image = ref.split()[0].lower()
        producto_proveedor, created = Proveedor.objects.get_or_create(nombre_proveedor= prov)
        nuevo_objeto_product = Producto(referencia=ref_mod, proveedor = producto_proveedor, cantidad_minima_reaprovisionamiento=cant_min,precio= random.randint(50, 150), cantidad_stock=20, imagen=f"media/{ref_image}.jpg")
        nuevo_objeto_product.save()
        producto_posicion_picking = ProductoPosicion(producto=nuevo_objeto_product, posicion=posicionesPicking )
        producto_posicion_stock = ProductoPosicion(producto=nuevo_objeto_product, posicion=posicionesStock )
        producto_posicion_picking.save()
        producto_posicion_stock.save()
        i+=1   
        

    #Asignar productos a posicion

if __name__ == "__main__":
    archivo_xlsx = "Proov_Ref_2023-1.xlsx"
    cargar_datos(archivo_xlsx)
    llenar_picking = Posicion.objects.filter(tipo_posicion="PIC").update(unidades_ocupadas=20)
    