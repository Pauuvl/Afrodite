from django.shortcuts import render

def catalogo(request):
    return render(request, 'catalogo/catalogo.html')