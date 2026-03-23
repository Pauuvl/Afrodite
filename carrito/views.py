from django.shortcuts import render

def cart_detail(request):
    return render(request, 'carrito/cart_detail.html')
