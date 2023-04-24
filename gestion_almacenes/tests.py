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