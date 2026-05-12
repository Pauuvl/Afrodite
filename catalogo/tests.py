# Autor: Helen Sanabria
"""
Pruebas unitarias del módulo catalogo.
Ejecutar con: python manage.py test catalogo
"""
from django.test import TestCase
from .models import Producto


class ProductoModelTest(TestCase):
    """Pruebas sobre el modelo Producto."""

    def setUp(self):
        self.producto = Producto.objects.create(
            nombre='Sérum Vitamina C',
            descripcion='Sérum antioxidante para todo tipo de piel.',
            precio='85000.00',
            categoria='skincare',
            tipo_piel='todos',
            stock=10,
        )

    def test_creacion_producto(self):
        """Un Producto recién creado debe existir en la base de datos."""
        self.assertIsNotNone(self.producto.pk)
        self.assertEqual(self.producto.nombre, 'Sérum Vitamina C')
        self.assertEqual(self.producto.categoria, 'skincare')

    def test_propiedad_agotado_con_stock(self):
        """agotado debe ser False cuando stock > 0."""
        self.assertFalse(self.producto.agotado)

    def test_propiedad_agotado_sin_stock(self):
        """agotado debe ser True cuando stock == 0."""
        self.producto.stock = 0
        self.producto.save()
        self.assertTrue(self.producto.agotado)

    def test_str_producto(self):
        """__str__ debe devolver el nombre del producto."""
        self.assertEqual(str(self.producto), 'Sérum Vitamina C')


class CarritoServicioTest(TestCase):
    """Pruebas unitarias sobre el servicio de carrito."""

    def setUp(self):
        from django.contrib.auth.models import User
        self.usuario = User.objects.create_user(
            username='testuser', password='testpass123'
        )
        self.producto = Producto.objects.create(
            nombre='Base Fluida',
            precio='120000.00',
            categoria='maquillaje',
            tipo_piel='todos',
            stock=5,
        )

    def test_agregar_producto_al_carrito(self):
        """Agregar un producto debe crear un CartItem y devolver éxito."""
        from carrito.services import agregar_al_carrito
        from carrito.models import CartItem

        exito, mensaje = agregar_al_carrito(self.usuario, self.producto.id, 1)

        self.assertTrue(exito)
        self.assertEqual(CartItem.objects.filter(
            cart__user=self.usuario, product=self.producto
        ).count(), 1)

    def test_agregar_producto_agotado_falla(self):
        """Agregar un producto sin stock debe devolver fracaso."""
        from carrito.services import agregar_al_carrito

        self.producto.stock = 0
        self.producto.save()

        exito, mensaje = agregar_al_carrito(self.usuario, self.producto.id, 1)

        self.assertFalse(exito)
        self.assertIn('agotado', mensaje.lower())