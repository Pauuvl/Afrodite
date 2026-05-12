# Autor: Viviana Arango Tabares

from django.contrib.auth.models import User
from django.test import TestCase

from catalogo.models import Producto
from catalogo.services import obtener_recomendados, obtener_recomendados_catalogo
from carrito.models import Cart, CartItem, Order, Payment
from carrito.services import agregar_producto_al_carrito, procesar_checkout


class ProductoTestCase(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='vivi',
            password='test123'
        )

        Producto.objects.create(
            nombre='Crema para piel grasa',
            precio=45000,
            categoria='skincare',
            tipo_piel='grasa',
            stock=5
        )

        Producto.objects.create(
            nombre='Bloqueador para todos',
            precio=60000,
            categoria='skincare',
            tipo_piel='todos',
            stock=8
        )

        Producto.objects.create(
            nombre='Crema para piel seca',
            precio=50000,
            categoria='skincare',
            tipo_piel='seca',
            stock=3
        )

    def test_producto_filtrado_por_tipo_piel(self):
        productos = Producto.objects.filter(tipo_piel__in=['grasa', 'todos'])
        nombres = [producto.nombre for producto in productos]

        self.assertIn('Crema para piel grasa', nombres)
        self.assertIn('Bloqueador para todos', nombres)
        self.assertNotIn('Crema para piel seca', nombres)

    def test_producto_en_stock(self):
        producto = Producto.objects.get(nombre='Crema para piel grasa')

        self.assertGreater(producto.stock, 0)


class RecomendacionesServiceTestCase(TestCase):

    def setUp(self):
        Producto.objects.create(
            nombre='Gel piel grasa',
            precio=40000,
            categoria='skincare',
            tipo_piel='grasa',
            stock=4
        )

        Producto.objects.create(
            nombre='Serum para todos',
            precio=70000,
            categoria='skincare',
            tipo_piel='todos',
            stock=6
        )

        Producto.objects.create(
            nombre='Hidratante piel seca',
            precio=55000,
            categoria='skincare',
            tipo_piel='seca',
            stock=2
        )

    def test_servicio_recomendaciones_retorna_tipo_piel_correcto(self):
        productos = obtener_recomendados('grasa')
        nombres = [producto.nombre for producto in productos]

        self.assertIn('Gel piel grasa', nombres)

    def test_servicio_recomendaciones_incluye_productos_para_todos(self):
        productos = obtener_recomendados_catalogo('grasa')
        nombres = [producto.nombre for producto in productos]

        self.assertIn('Serum para todos', nombres)
        self.assertNotIn('Hidratante piel seca', nombres)


class CheckoutServiceTestCase(TestCase):

    def setUp(self):
        self.usuario = User.objects.create_user(
            username='comprador',
            password='test123'
        )

        self.producto = Producto.objects.create(
            nombre='Labial mate',
            precio=35000,
            categoria='maquillaje',
            tipo_piel='todos',
            stock=10
        )

    def test_checkout_crea_order_y_payment(self):
        agregar_producto_al_carrito(
            user=self.usuario,
            product_id=self.producto.id,
            quantity=2
        )

        cart = Cart.objects.get(user=self.usuario, is_active=True)

        order = procesar_checkout(
            user=self.usuario,
            cart=cart,
            metodo_pago='card'
        )

        self.assertIsNotNone(order.id)
        self.assertEqual(Order.objects.count(), 1)
        self.assertEqual(Payment.objects.count(), 1)

    def test_checkout_desactiva_carrito(self):
        agregar_producto_al_carrito(
            user=self.usuario,
            product_id=self.producto.id,
            quantity=1
        )

        cart = Cart.objects.get(user=self.usuario, is_active=True)

        procesar_checkout(
            user=self.usuario,
            cart=cart,
            metodo_pago='transfer'
        )

        cart.refresh_from_db()

        self.assertFalse(cart.is_active)

    def test_checkout_descuenta_stock(self):
        agregar_producto_al_carrito(
            user=self.usuario,
            product_id=self.producto.id,
            quantity=3
        )

        cart = Cart.objects.get(user=self.usuario, is_active=True)

        procesar_checkout(
            user=self.usuario,
            cart=cart,
            metodo_pago='card'
        )

        self.producto.refresh_from_db()

        self.assertEqual(self.producto.stock, 7)