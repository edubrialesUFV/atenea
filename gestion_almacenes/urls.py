from django.urls import path
from . import views


urlpatterns = [
   path('detail/<str:id>/', views.producto_detail, name="detail"),
   path('cesta/<str:id>/', views.anadirAcesta, name="cesta"),
]
