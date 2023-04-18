import os
import sys
import django
import openpyxl
from django.core.exceptions import ValidationError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "atenea.settings")
django.setup()

from gestion_almacenes.models import Proveedor, Producto

def cargar_datos(archivo_xlsx):
    wb = openpyxl.load_workbook(archivo_xlsx)
    hoja = wb['Hoja1']

    # Asumiendo que la primera fila tiene encabezados y los datos comienzan en la segunda fila
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        prov, ref, cant_min = fila
        ref = ref.lower()
        ref = ref.replace(" ", "_")
        producto_proveedor, created = Proveedor.objects.get_or_create(nombre_proveedor= prov)
        nuevo_objeto_product = Producto(referencia=ref, proveedor = producto_proveedor, cantidad_minima_reaprovisionamiento=cant_min)
        try:
            nuevo_objeto_product.full_clean()
            nuevo_objeto_product.save()
            print(f"Objeto creado: {nuevo_objeto_product}")
        except ValidationError as e:
            print(f"Error al crear objeto: {e}")
            
            
       

if __name__ == "__main__":
    archivo_xlsx = "Proov_Ref_2023-1.xlsx"
    cargar_datos(archivo_xlsx)