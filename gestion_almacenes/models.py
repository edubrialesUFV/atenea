from django.db import models

from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class ClienteManager(BaseUserManager):
    def create_user(self, nombre_cliente, email, password=None, **extra_fields):
        if not email:
            raise ValueError('El campo email es obligatorio.')
        email = self.normalize_email(email)
        user = self.model(nombre_cliente=nombre_cliente, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombre_cliente, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(nombre_cliente, email, password, **extra_fields)
    
class Cliente(AbstractBaseUser, PermissionsMixin):
    nombre_cliente = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    direccion_cliente = models.CharField(max_length=150)
    codigo_postal = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = ClienteManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre_cliente']

    def __str__(self):
        return self.nombre_cliente

class Proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_proveedor


class Producto(models.Model):
    referencia = models.CharField(max_length=20)
    # nombre_producto = models.CharField(max_length=100)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    cantidad_stock = models.PositiveIntegerField(default=0)
    cantidad_minima_reaprovisionamiento = models.PositiveIntegerField()
    precio = models.PositiveIntegerField(default=0)
    peso_por_unidad = models.FloatField(default=200)
    imagen = models.ImageField(upload_to='media/', blank= True, null= True )


    def __str__(self):
        return self.referencia



class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_hora_pedido = models.DateTimeField()
    TIPO_ENVIO_CHOICES = [
        ('EST', 'Estándar'),
        ('URG', 'Urgente'),
    ]
    tipo_envio = models.CharField(max_length=3, choices=TIPO_ENVIO_CHOICES)
    AGENCIA_TRANSPORTE_CHOICES = [
        ('COR', 'Correos'),
        ('SEU', 'Seur'),
        ('DHL', 'DHL'),
    ]
    agencia_transporte = models.CharField(max_length=3, choices=AGENCIA_TRANSPORTE_CHOICES)
    etiqueta = models.ImageField(upload_to='media/etiquetas/', blank= True, null= True )
    albaran = models.FileField(upload_to='media/albaranes/', blank= True, null= True)
    def __str__(self):
        return f"{self.cliente} - {self.fecha_hora_pedido}"


class PedidoProducto(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.pedido} - {self.producto}"


class Posicion(models.Model):
    TIPO_POSICION_CHOICES = [
        ('PIC', 'Picking'),
        ('STO', 'Stock'),
    ]
    id = models.CharField(max_length=6, primary_key=True)
    tipo_posicion = models.CharField(max_length=3, choices=TIPO_POSICION_CHOICES)
    capacidad = models.PositiveIntegerField()
    unidades_ocupadas = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.tipo_posicion} - {self.id}"


class ProductoPosicion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    posicion = models.ForeignKey(Posicion, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.producto} - {self.posicion}"