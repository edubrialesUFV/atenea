from django.urls import path
from . import views


urlpatterns = [
   path('<str:id>', views.producto_detail, name="detail"),
   path('<str:id>', views.anadirAcesta, name="cesta"),
]
