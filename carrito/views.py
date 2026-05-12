# Autor: Viviana Arango Tabares y Helen Sanabria

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render

from .models import Cart, CartItem
from . import services


@login_required
def detalle_carrito(request):
    from catalogo.models import Producto
    carrito = services.obtener_o_crear_carrito(request.user)
    items   = CartItem.objects.filter(cart=carrito)
    productos = Producto.objects.all().order_by('categoria', 'nombre')
    total   = services.calcular_total(items)

    return render(request, 'carrito/cart_detail.html', {
        'cart':     carrito,
        'items':    items,
        'products': productos,
        'total':    total,
    })


@login_required
def agregar_producto(request):
    if request.method == 'POST':
        producto_id = request.POST.get('product_id')
        cantidad    = int(request.POST.get('quantity', 1))
        exito, mensaje = services.agregar_al_carrito(request.user, producto_id, cantidad)
        codigo = 200 if exito else 400
        return JsonResponse({'success': exito, 'message': mensaje}, status=codigo)

    return JsonResponse({'success': False, 'message': 'Método no permitido.'}, status=405)


@login_required
def actualizar_item(request, item_id):
    if request.method == 'POST':
        cantidad = int(request.POST.get('quantity', 1))
        services.actualizar_item_carrito(request.user, item_id, cantidad)
    return redirect('carrito:detalle_carrito')


@login_required
def eliminar_item(request, item_id):
    if request.method == 'POST':
        services.eliminar_item_carrito(request.user, item_id)
    return redirect('carrito:detalle_carrito')


@login_required
def checkout(request):
    carrito = get_object_or_404(Cart, user=request.user, is_active=True)
    items   = CartItem.objects.filter(cart=carrito)
    total   = services.calcular_total(items)

    if not items.exists():
        return redirect('carrito:detalle_carrito')

    if request.method == 'POST':
        metodo = request.POST.get('method')
        services.procesar_checkout(request.user, metodo)
        return redirect('carrito:pago_exitoso')

    return render(request, 'carrito/checkout.html', {
        'cart':  carrito,
        'items': items,
        'total': total,
    })


@login_required
def pago_exitoso(request):
    return render(request, 'carrito/payment_success.html')