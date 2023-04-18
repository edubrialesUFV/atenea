from django.urls import path
from . import views


urlpatterns = [
   path('<str:id>', views.producto_detail, name="detail"),
   path('mostrar_productos/', views.mostrar_productos, name='mostrar_productos'),
]
