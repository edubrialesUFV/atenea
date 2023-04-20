"""atenea URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from gestion_almacenes import views, admin
from gestion_almacenes.views import checkout, procesar_compra, eliminar_producto

urlpatterns = [
    path('admin/registrar_producto/', views.registrar_producto, name="registrar_producto"),
    path('admin/', admin.my_admin_site.urls),
    path('', views.index, name="home"),
    path("producto/", include("gestion_almacenes.urls")),
    path('register/', views.register, name="register"),
    path('login/', views.ClienteLoginView.as_view(), name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('checkout/', checkout, name='checkout'),
    path('checkout/procesar_compra/', procesar_compra, name='procesar_compra'),
    path('eliminar/<int:producto_id>/', eliminar_producto, name='eliminar_producto'),

]
