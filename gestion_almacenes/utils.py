


def pedir_proveedores(producto):
    if producto.cantidad_stock < producto.cantidad_minima_reaprovisionamiento:
        producto.cantidad_stock=+ 20



