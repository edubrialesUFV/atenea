from django.urls import path
from django.contrib import admin
from . import views
from gestion_almacenes.models import Producto, Cliente, Pedido, Proveedor, ProductoPosicion, Posicion, PedidoProducto

class MyAdminSite(admin.AdminSite):
    site_header = 'My Administration'
    index_template = 'admin_custom.html'

my_admin_site = MyAdminSite()

class PedidoAdmin(admin.ModelAdmin):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('pedidos_productos/', self.admin_site.admin_view(views.pedidos_productos), name='pedidos_productos'),
        ]
        return custom_urls + urls

my_admin_site.register(Producto)
my_admin_site.register(Cliente)
my_admin_site.register(Pedido, PedidoAdmin)  # Registra la clase PedidoAdmin junto con el modelo Pedido
my_admin_site.register(Proveedor)
my_admin_site.register(ProductoPosicion)
my_admin_site.register(Posicion)
my_admin_site.register(PedidoProducto)
