#Autor: Helen Sanabria
from .models import Producto

def obtener_tipo_piel_usuario(request):
    """Obtiene el tipo de piel del usuario autenticado"""
    if request.user.is_authenticated:
        try:
            tipo = request.user.perfil.tipo_piel
            return tipo if tipo else None
        except Exception:
            return None
    return None

def obtener_skincare():
    """Obtiene todos los productos de skincare"""
    return Producto.objects.filter(categoria='skincare')

def obtener_maquillaje():
    """Obtiene todos los productos de maquillaje"""
    return Producto.objects.filter(categoria='maquillaje')

def obtener_recomendados(tipo_piel, limite=4):
    """Obtiene productos recomendados según tipo de piel"""
    if tipo_piel:
        return Producto.objects.filter(
            tipo_piel__in=[tipo_piel, 'todos']
        )[:limite]
    return []

def obtener_recomendados_catalogo(tipo_piel):
    """Obtiene recomendados para el catálogo (sin límite)"""
    if tipo_piel:
        return list(Producto.objects.filter(tipo_piel__in=[tipo_piel, 'todos']))
    return []

def obtener_productos_disponibles():
    """Todos los productos disponibles para API (stock > 0)"""
    return Producto.objects.filter(stock__gt=0)