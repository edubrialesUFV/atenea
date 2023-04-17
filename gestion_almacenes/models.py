from django.db import models


class Proveedor(models.Model):
    nombre_proveedor = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre_proveedor


class Producto(models.Model):
    referencia = models.CharField(max_length=20)
    # nombre_producto = models.CharField(max_length=100)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    cantidad_stock = models.PositiveIntegerField(null=True, blank=True)
    cantidad_minima_reaprovisionamiento = models.PositiveIntegerField()
    peso_por_unidad = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.referencia


class Cliente(models.Model):
    nombre_cliente = models.CharField(max_length=100)
    direccion_cliente = models.CharField(max_length=150)
    codigo_postal = models.CharField(max_length=10)

    def __str__(self):
        return self.nombre_cliente


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
    tipo_posicion = models.CharField(max_length=3, choices=TIPO_POSICION_CHOICES)
    capacidad = models.PositiveIntegerField()
    unidades_ocupadas = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.tipo_posicion} - {self.id}"


class ProductoPosicion(models.Model):
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    posicion = models.ForeignKey(Posicion, on_delete=models.CASCADE)
    cantidad_almacenada = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.producto} - {self.posicion}"