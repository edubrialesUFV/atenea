from django.urls import path
from . import views


urlpatterns = [
   path('detail/<str:id>/', views.producto_detail, name="detail"),
   path('cesta/<str:id>/', views.anadirAcesta, name="cesta"),
   path('admin/pedidos_productos/', views.pedidos_productos, name='pedidos_productos'),
   
]
