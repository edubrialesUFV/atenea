from django.shortcuts import resolve_url
from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse
from io import BytesIO

from requests import request
from .models import Producto, Cliente, Pedido, Proveedor
from .views import procesar_compra, generar_pdf
import os
from django.test import TestCase, Client
from django.contrib.auth.models import AnonymousUser
from gestion_almacenes.models import Cliente, Producto, Proveedor
from gestion_almacenes.views import procesar_compra
from gestion_almacenes.models import Cliente, Producto
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages

class ProcesarCompraTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = Cliente.objects.create_user(
            nombre_cliente='John Doe',
            email='john@example.com',
            password='password123',
            direccion_cliente='123 Test Street',
            codigo_postal='12345'
        )

        self.proveedor = Proveedor.objects.create(nombre_proveedor='Proveedor Test')

        self.producto = Producto.objects.create(
            referencia='REF123',
            proveedor=self.proveedor,
            cantidad_stock=10,
            cantidad_minima_reaprovisionamiento=2,
            precio=100,
            peso_por_unidad=200,
        )

    def test_procesar_compra(self):
        # Asegúrate de que estás proporcionando todos los campos necesarios en los datos de la solicitud POST
        self.client.login(username='john@example.com', password='password123')
        response = self.client.post('/checkout/procesar_compra/', {
            'tipo_envio': 'EST',
            'agencia_transporte': 'COR',
            'carrito': {
                str(self.producto.id): {
                    'cantidad': 1
                }
            }
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

        self.assertEqual(Pedido.objects.count(), 1)

        # Realiza más comprobaciones aquí, como verificar que el PDF se haya creado correctamente.

class GenerarPdfTest(TestCase):
    def test_generar_pdf(self):
        template_src = "comprobanteDHL.html"
        context_dict = {
            # Agrega tus datos de prueba aquí
        }
        output_filename = "test_pdf_output.pdf"

        pdf_data = generar_pdf(template_src, context_dict, output_filename)

        self.assertIsNotNone(pdf_data)

        # Comprueba si el archivo PDF se ha creado correctamente.
        with open(output_filename, "rb") as f:
            file_data = f.read()
        self.assertEqual(pdf_data, file_data)

        # Elimina el archivo PDF de prueba.
        os.remove(output_filename)



class EliminarProductoTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.producto1 = Producto.objects.create(
            referencia='ABC123',
            proveedor=Proveedor.objects.create(nombre_proveedor='Proveedor 1'),
            cantidad_stock=50,
            cantidad_minima_reaprovisionamiento=10,
            precio=100,
            peso_por_unidad=200,
        )

        self.producto2 = Producto.objects.create(
            referencia='DEF456',
            proveedor=Proveedor.objects.create(nombre_proveedor='Proveedor 2'),
            cantidad_stock=20,
            cantidad_minima_reaprovisionamiento=5,
            precio=200,
            peso_por_unidad=150,
        )

        self.user = get_user_model().objects.create_user(
            nombre_cliente='John Doe',
            email='john@example.com',
            password='password123',
        )

    def test_eliminar_producto(self):
        # Iniciar sesión y agregar productos al carrito
        self.client.login(username='john@example.com', password='password123')
        session = self.client.session
        session['carrito'] = {
            str(self.producto1.id): {'cantidad': 1},
            str(self.producto2.id): {'cantidad': 2},
        }
        session.save()

        # Eliminar el producto1 del carrito
        response = self.client.post(reverse('eliminar_producto', args=[self.producto1.id]))

        # Comprobar si el producto1 ha sido eliminado correctamente
        self.assertEqual(response.status_code, 302)  # Verificar que la redirección se haya realizado correctamente
        self.assertNotIn(str(self.producto1.id), self.client.session['carrito'])  # Verificar que el producto1 ya no está en el carrito
        self.assertIn(str(self.producto2.id), self.client.session['carrito'])  # Verificar que el producto2 sigue en el carrito

class AnadirACestaTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.proveedor = Proveedor.objects.create(nombre_proveedor='Proveedor 1')

        self.producto = Producto.objects.create(
            referencia='ABC123',
            proveedor=self.proveedor,
            cantidad_stock=50,
            cantidad_minima_reaprovisionamiento=10,
            precio=100,
            peso_por_unidad=200,
        )

    def test_anadir_a_cesta(self):
        # Añadir el producto al carrito con una cantidad válida
        response = self.client.post(reverse('cesta', args=[self.producto.referencia]), {'cantidad': 2})
        self.assertEqual(response.status_code, 302)  # Verificar que la redirección se haya realizado correctamente
        self.assertIn(str(self.producto.id), self.client.session['carrito'])  # Verificar que el producto está en el carrito

        # Comprobar el mensaje de éxito
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]), f'2 unidades de {self.producto.referencia.split("_")[0].capitalize()} han sido añadidas al carrito')

        # Añadir el producto al carrito con una cantidad no válida
        response = self.client.post(reverse('cesta', args=[self.producto.referencia]), {'cantidad': self.producto.cantidad_stock + 1})
        self.assertEqual(response.status_code, 302)  # Verificar que se realiza la redirección correctamente

        # Comprobar el mensaje de error
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        # self.assertEqual(str(messages[0]), f'Sólo hay {self.producto.cantidad_stock} unidades disponibles')




class CheckoutTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.proveedor = Proveedor.objects.create(nombre_proveedor='Proveedor 1')

        self.producto = Producto.objects.create(
            referencia='ABC123',
            proveedor=self.proveedor,
            cantidad_stock=50,
            cantidad_minima_reaprovisionamiento=10,
            precio=100,
            peso_por_unidad=200,
        )

    def test_checkout(self):
        # Añadir el producto al carrito
        carrito = {str(self.producto.id): {'referencia': self.producto.referencia, 'cantidad': 2}}
        session = self.client.session
        session['carrito'] = carrito
        session.save()

        # Acceder a la página de checkout
        response = self.client.get(reverse('checkout'))

        # Comprobar que se carga la página correctamente
        self.assertEqual(response.status_code, 200)

        # Verificar que el producto está en la lista de productos del contexto
        self.assertEqual(len(response.context['productos']), 1)
        self.assertEqual(response.context['productos'][0]['id'], self.producto.id)
        self.assertEqual(response.context['productos'][0]['cantidad'], 2)
        self.assertEqual(response.context['productos'][0]['precio'], self.producto.id)
        self.assertEqual(response.context['productos'][0]['subtotal'], self.producto.id * 2)

        # Verificar que el total es correcto
        self.assertEqual(response.context['total'], self.producto.id * 2)