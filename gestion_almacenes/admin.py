from django.contrib import admin
from gestion_almacenes.models import Producto, Cliente, Pedido, Proveedor, ProductoPosicion, Posicion
# Register your models here.

class MyAdminSite(admin.AdminSite):
    site_header = 'My Administration'
    index_template = 'admin_custom.html'

my_admin_site = MyAdminSite()

# class AuthorAdmin(admin.ModelAdmin):

my_admin_site.register(Producto)


