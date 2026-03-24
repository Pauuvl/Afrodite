from django.shortcuts import render
from .models import Producto

def index(request):
    skincare    = Producto.objects.filter(categoria='skincare')[:5]
    maquillaje  = Producto.objects.filter(categoria='maquillaje')[:5]
    return render(request, 'index.html', {
        'skincare': skincare,
        'maquillaje': maquillaje
    })

def catalogo(request):
    skincare    = Producto.objects.filter(categoria='skincare')
    maquillaje  = Producto.objects.filter(categoria='maquillaje')
    return render(request, 'catalogo/catalogo.html', {
        'skincare': skincare,
        'maquillaje': maquillaje
    })