from .models import Producto, Posicion, ProductoPosicion

def migrations_picstock(productos):
    for producto_dict in productos:
        print(producto_dict)
        producto_dd =  producto_dict['producto']
        cantidad = producto_dict['cantidad']
        posiciones = ProductoPosicion.objects.filter(producto = producto_dd).order_by("posicion")
        posicion_picking = Posicion.objects.get(id = posiciones[0].posicion.id)
        posicion_stock = Posicion.objects.get(id = posiciones[1].posicion.id)
        posicion_picking.unidades_ocupadas = posicion_picking.unidades_ocupadas - cantidad
        posicion_picking.save()
        if posicion_picking.unidades_ocupadas == 0:
            posicion_picking.unidades_ocupadas = posicion_stock.unidades_ocupadas
            posicion_stock.unidades_ocupadas = 0
            posicion_picking.save()
            posicion_stock.save()


def pedir_proveedores(productos):
    for producto_dict in productos:
        print(producto_dict)
        producto_dd =  producto_dict['producto']
        if producto_dd.cantidad_stock < producto_dd.cantidad_minima_reaprovisionamiento:
            producto_dd.cantidad_stock = producto_dd.cantidad_stock + 20
            producto_dd.save()
            posiciones = ProductoPosicion.objects.filter(producto = producto_dd).order_by("posicion")
            posicion_picking = Posicion.objects.get(id = posiciones[0].posicion.id)
            posicion_stock = Posicion.objects.get(id = posiciones[1].posicion.id)
            posicion_stock.unidades_ocupadas = posicion_stock.unidades_ocupadas + posicion_picking.unidades_ocupadas
            posicion_stock.save()
            posicion_picking.unidades_ocupadas = 20
            posicion_picking.save()
            



