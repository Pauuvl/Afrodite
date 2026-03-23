from django.shortcuts import render

# Página principal
def index(request):
    return render(request, 'index.html')

# Página catálogo
def catalogo(request):
    return render(request, 'catalogo.html')