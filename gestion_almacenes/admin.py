from django.contrib import admin
from gestion_almacenes.models import Producto, Cliente, Pedido, Proveedor, ProductoPosicion, Posicion, PedidoProducto
# Register your models here.

class MyAdminSite(admin.AdminSite):
    site_header = 'My Administration'
    index_template = 'admin_custom.html'

my_admin_site = MyAdminSite()

# class AuthorAdmin(admin.ModelAdmin):

my_admin_site.register(Producto)
my_admin_site.register(Cliente)
my_admin_site.register(Pedido)
my_admin_site.register(Proveedor)
my_admin_site.register(ProductoPosicion)
my_admin_site.register(Posicion)
my_admin_site.register(PedidoProducto)


