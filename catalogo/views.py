<<<<<<< HEAD
# Autor: Paulina Velasquez Londoño
from django.shortcuts import render
from .models import Producto

# ── HELPERS ──────────────────────────────────────────────────
def get_tipo_piel_usuario(request):
    if request.user.is_authenticated:
        try:
            tipo = request.user.perfil.tipo_piel
            return tipo if tipo else None   # evita string vacío '' que es falsy pero pasa el try
        except Exception:
            return None
    return None

# ── VISTAS PRINCIPALES ────────────────────────────────────────
=======
# Autor: Paulina Velasquez Londoño y Helen Sanabria
from django.http import JsonResponse
from django.shortcuts import render
from .services import (
    obtener_tipo_piel_usuario,
    obtener_skincare,
    obtener_maquillaje,
    obtener_recomendados,
    obtener_recomendados_catalogo,
    obtener_productos_disponibles,
)


>>>>>>> origin/main
def index(request):
    tipo_piel    = obtener_tipo_piel_usuario(request)
    skincare     = obtener_skincare()[:4]
    maquillaje   = obtener_maquillaje()[:4]
    recomendados = obtener_recomendados(tipo_piel, 4)

    return render(request, 'index.html', {
        'skincare':     skincare,
        'maquillaje':   maquillaje,
        'recomendados': recomendados,
        'tipo_piel':    tipo_piel,
    })


def catalogo(request):
    tipo_piel    = obtener_tipo_piel_usuario(request)
    skincare     = obtener_skincare()
    maquillaje   = obtener_maquillaje()
    recomendados = obtener_recomendados_catalogo(tipo_piel)

    return render(request, 'catalogo/catalogo.html', {
        'skincare':     skincare,
        'maquillaje':   maquillaje,
        'recomendados': recomendados,
        'tipo_piel':    tipo_piel,
    })


def api_productos(request):
    """Servicio web que provee información de productos en formato JSON"""
    productos = obtener_productos_disponibles()
    data = {
        'count': productos.count(),
        'productos': [
            {
                'id': p.id,
                'nombre': p.nombre,
                'precio': str(p.precio),
                'categoria': p.categoria,
                'tipo_piel': p.tipo_piel,
                'stock': p.stock,
                'descripcion': p.descripcion,
                'imagen_url': p.imagen.url if p.imagen else None,
                'enlace_detalle': f'/catalogo/?producto={p.id}',
            }
            for p in productos
        ],
    }
    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})