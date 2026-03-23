from decimal import Decimal
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Cart, CartItem, Order, Payment


@login_required
def cart_detail(request):
    cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)
    items = CartItem.objects.filter(cart=cart)

    total = sum(item.unit_price * item.quantity for item in items)

    return render(request, 'carrito/cart_detail.html', {
        'cart': cart,
        'items': items,
        'total': total,
    })


@login_required
def add_to_cart(request):
    if request.method == 'POST':
        product_name = request.POST.get('product_name')
        unit_price = request.POST.get('unit_price')
        quantity = int(request.POST.get('quantity', 1))

        cart, created = Cart.objects.get_or_create(user=request.user, is_active=True)

        existing_item = CartItem.objects.filter(
            cart=cart,
            product_name=product_name,
            unit_price=Decimal(unit_price)
        ).first()

        if existing_item:
            existing_item.quantity += quantity
            existing_item.save()
        else:
            CartItem.objects.create(
                cart=cart,
                product_name=product_name,
                unit_price=Decimal(unit_price),
                quantity=quantity
            )

    return redirect('cart_detail')


@login_required
def update_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user, cart__is_active=True)

    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))

        if quantity > 0:
            item.quantity = quantity
            item.save()
        else:
            item.delete()

    return redirect('cart_detail')


@login_required
def remove_cart_item(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, cart__user=request.user, cart__is_active=True)

    if request.method == 'POST':
        item.delete()

    return redirect('cart_detail')


@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user, is_active=True)
    items = CartItem.objects.filter(cart=cart)
    total = sum(item.unit_price * item.quantity for item in items)

    if not items.exists():
        return redirect('cart_detail')

    if request.method == 'POST':
        method = request.POST.get('method')

        order = Order.objects.create(
            user=request.user,
            total=total,
            status='paid'
        )

        Payment.objects.create(
            order=order,
            method=method,
            status='completed',
            transaction_id=f"TXN-{order.id}-{request.user.id}"
        )

        cart.is_active = False
        cart.save()

        return redirect('payment_success')

    return render(request, 'carrito/checkout.html', {
        'cart': cart,
        'items': items,
        'total': total,
    })


@login_required
def payment_success(request):
    return render(request, 'carrito/payment_success.html')