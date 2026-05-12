# Autor: Helen Sanabria
"""
Servicios de negocio del carrito.
Las vistas solo llaman a estas funciones; no contienen lógica propia.
"""
from catalogo.models import Producto
from .models import Cart, CartItem, Order, OrderItem, Payment

# ── Carrito ────────────────────────────────────────────────────────────────

def obtener_o_crear_carrito(usuario):
    """Devuelve el carrito activo del usuario, creándolo si no existe."""
    carrito, _ = Cart.objects.get_or_create(user=usuario, is_active=True)
    return carrito


def calcular_total(items):
    """Calcula el total de una lista/queryset de CartItem."""
    return sum(
        (item.product.precio if item.product else item.unit_price) * item.quantity
        for item in items
    )


def agregar_al_carrito(usuario, producto_id, cantidad=1):
    """
    Agrega un producto al carrito del usuario.
    Devuelve (éxito: bool, mensaje: str).
    """
    try:
        producto = Producto.objects.get(id=producto_id)
    except Producto.DoesNotExist:
        return False, 'Producto no encontrado.'

    if producto.agotado:
        return False, f'El producto "{producto.nombre}" está agotado.'

    carrito = obtener_o_crear_carrito(usuario)
    item_existente = CartItem.objects.filter(cart=carrito, product=producto).first()
    cantidad_actual = item_existente.quantity if item_existente else 0

    if cantidad_actual + cantidad > producto.stock:
        return False, f'Solo hay {producto.stock} unidades disponibles de "{producto.nombre}".'

    if item_existente:
        item_existente.quantity += cantidad
        item_existente.save()
    else:
        CartItem.objects.create(cart=carrito, product=producto, quantity=cantidad)

    return True, 'El producto se ha agregado al carrito.'


def actualizar_item_carrito(usuario, item_id, cantidad):
    """
    Actualiza la cantidad de un ítem. Si cantidad <= 0 lo elimina.
    Devuelve el item o None si fue eliminado.
    """
    item = CartItem.objects.filter(
        id=item_id,
        cart__user=usuario,
        cart__is_active=True,
    ).first()

    if item is None:
        return None

    if cantidad > 0:
        item.quantity = cantidad
        item.save()
        return item
    else:
        item.delete()
        return None


def eliminar_item_carrito(usuario, item_id):
    """Elimina un ítem del carrito del usuario."""
    CartItem.objects.filter(
        id=item_id,
        cart__user=usuario,
        cart__is_active=True,
    ).delete()

# ── Checkout ───────────────────────────────────────────────────────────────

def procesar_checkout(usuario, metodo_pago):
    """
    Crea la Order, los OrderItem, actualiza stock, registra el Payment
    y desactiva el carrito.
    Devuelve la Order creada.
    """
    carrito = Cart.objects.get(user=usuario, is_active=True)
    items = CartItem.objects.filter(cart=carrito)
    total = calcular_total(items)

    orden = Order.objects.create(user=usuario, total=total, status='paid')

    for item in items:
        producto = item.product
        precio = producto.precio if producto else item.unit_price

        OrderItem.objects.create(
            order=orden,
            product=producto,
            product_name=producto.nombre if producto else (item.product_name or ''),
            unit_price=precio,
            quantity=item.quantity,
        )

        if producto and producto.stock > 0:
            producto.stock = max(0, producto.stock - item.quantity)
            producto.save(update_fields=['stock'])

    Payment.objects.create(
        order=orden,
        method=metodo_pago,
        status='completed',
        transaction_id=f'TXN-{orden.id}-{usuario.id}',
    )

    carrito.is_active = False
    carrito.save()

    return orden