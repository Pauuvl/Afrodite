# Autor: Viviana Arango Tabares y Helen Sanabria

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from catalogo.models import Producto
from .models import CartItem
from .services import (
    agregar_producto_al_carrito,
    actualizar_item_carrito,
    calcular_total,
    eliminar_item_carrito,
    obtener_carrito_activo,
    procesar_checkout,
)


@login_required
def cart_detail(request):
    cart = obtener_carrito_activo(request.user)
    items = CartItem.objects.filter(cart=cart).select_related('product')
    products = Producto.objects.all().order_by('categoria', 'nombre')
    total = calcular_total(cart)

    return render(request, 'carrito/cart_detail.html', {
        'cart':     cart,
        'items':    items,
        'products': products,
        'total':    total,
    })


@login_required
def agregar_producto(request):
    if request.method == 'POST':
        producto_id = request.POST.get('product_id')
        cantidad = int(request.POST.get('quantity', 1))

        exito, mensaje = agregar_producto_al_carrito(
            request.user,
            producto_id,
            cantidad
        )

        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': exito,
                'message': mensaje
            }, status=200 if exito else 400)

        return redirect('carrito:cart_detail')

    return JsonResponse({
        'success': False,
        'message': 'Método no permitido.'
    }, status=405)


@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        actualizar_item_carrito(request.user, item_id, quantity)

    return redirect('carrito:cart_detail')


@login_required
def remove_cart_item(request, item_id):
    if request.method == 'POST':
        eliminar_item_carrito(request.user, item_id)

    return redirect('carrito:cart_detail')


@login_required
def checkout(request):
    cart = obtener_carrito_activo(request.user)
    items = CartItem.objects.filter(cart=cart).select_related('product')
    total = calcular_total(cart)

    if not items.exists():
        return redirect('carrito:cart_detail')

    if request.method == 'POST':
        metodo_pago = request.POST.get('method')
        procesar_checkout(request.user, cart, metodo_pago)
        return redirect('carrito:payment_success')

    return render(request, 'carrito/checkout.html', {
        'cart':  cart,
        'items': items,
        'total': total,
    })


@login_required
def pago_exitoso(request):
    return render(request, 'carrito/payment_success.html')