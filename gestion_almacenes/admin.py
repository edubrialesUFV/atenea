from django.contrib import admin
from gestion_almacenes.models import Producto, Cliente, Pedido, Proveedor, ProductoPosicion, Posicion
# Register your models here.



# class AuthorAdmin(admin.ModelAdmin):
#     pass

admin.site.register(Proveedor)
admin.site.register(Producto)
admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(Posicion)
