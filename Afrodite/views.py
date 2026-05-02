from django.shortcuts import render

def index(request):
    return render(request, 'index.html')

def catalogo(request):
    return render(request, 'catalogo/catalogo.html')