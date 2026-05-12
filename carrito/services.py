
# Autor: Viviana Arango y Helen Sanabria

from django.db import transaction
from django.shortcuts import get_object_or_404
from catalogo.models import Producto
from .models import Cart, CartItem, Order, OrderItem, Payment


def obtener_carrito_activo(user):
    cart, created = Cart.objects.get_or_create(user=user, is_active=True)
    return cart


def calcular_total(cart):
    items = CartItem.objects.filter(cart=cart)
    return sum(item.product.precio * item.quantity for item in items)


def agregar_producto_al_carrito(user, product_id, quantity=1):
    product = get_object_or_404(Producto, id=product_id)

    if product.agotado:
        return False, f'El producto "{product.nombre}" está agotado.'

    cart = obtener_carrito_activo(user)

    item = CartItem.objects.filter(cart=cart, product=product).first()
    cantidad_actual = item.quantity if item else 0

    if cantidad_actual + quantity > product.stock:
        return False, f'Solo hay {product.stock} unidades disponibles de "{product.nombre}".'

    if item:
        item.quantity += quantity
        item.save()
    else:
        CartItem.objects.create(
            cart=cart,
            product=product,
            quantity=quantity
        )

    return True, 'El producto se ha agregado al carrito.'


def actualizar_item_carrito(user, item_id, quantity):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=user,
        cart__is_active=True
    )

    if quantity > 0:
        item.quantity = quantity
        item.save()
    else:
        item.delete()

    return item


def eliminar_item_carrito(user, item_id):
    item = get_object_or_404(
        CartItem,
        id=item_id,
        cart__user=user,
        cart__is_active=True
    )
    item.delete()


@transaction.atomic
def procesar_checkout(user, cart, metodo_pago):
    items = CartItem.objects.select_related('product').filter(cart=cart)

    if not items.exists():
        raise ValueError('El carrito está vacío.')

    total = calcular_total(cart)

    order = Order.objects.create(
        user=user,
        total=total,
        status='paid'
    )

    for item in items:
        product = item.product

        OrderItem.objects.create(
            order=order,
            product=product,
            product_name=product.nombre,
            unit_price=product.precio,
            quantity=item.quantity
        )

        product.stock = max(0, product.stock - item.quantity)
        product.save(update_fields=['stock'])

    Payment.objects.create(
        order=order,
        method=metodo_pago,
        status='completed',
        transaction_id=f"TXN-{order.id}-{user.id}"
    )

    cart.is_active = False
    cart.save(update_fields=['is_active'])

    return order
