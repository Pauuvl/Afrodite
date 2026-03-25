# Autor: Paulina Velasquez Londoño
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Producto

# ── CARRITO (sesión) ──────────────────────────────────────────
def get_carrito(request):
    return request.session.get('carrito', {})

def save_carrito(request, carrito):
    request.session['carrito'] = carrito
    request.session.modified = True

def agregar_carrito(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    carrito  = get_carrito(request)
    key      = str(producto_id)
    if key in carrito:
        carrito[key]['cantidad'] += 1
    else:
        carrito[key] = {
            'nombre':   producto.nombre,
            'precio':   float(producto.precio),
            'cantidad': 1,
            'imagen':   producto.imagen.url if producto.imagen else '',
        }
    save_carrito(request, carrito)
    messages.success(request, f'"{producto.nombre}" agregado al carrito ✓')
    return redirect(request.META.get('HTTP_REFERER', 'catalogo'))

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
def index(request):
    tipo_piel     = get_tipo_piel_usuario(request)
    skincare      = Producto.objects.filter(categoria='skincare')
    maquillaje    = Producto.objects.filter(categoria='maquillaje')

    # Recomendados: productos que coincidan con tipo de piel del usuario
    recomendados  = []
    if tipo_piel:
        recomendados = Producto.objects.filter(
            tipo_piel__in=[tipo_piel, 'todos']
        )[:4]

    return render(request, 'index.html', {
        'skincare':    skincare[:4],
        'maquillaje':  maquillaje[:4],
        'recomendados': recomendados,
        'tipo_piel':   tipo_piel,
    })

def catalogo(request):
    tipo_piel  = get_tipo_piel_usuario(request)
    skincare   = Producto.objects.filter(categoria='skincare')
    maquillaje = Producto.objects.filter(categoria='maquillaje')

    # Recomendados: filtra por tipo de piel del usuario + productos para "todos"
    # Si tipo_piel es None o vacío, recomendados queda vacío (usuario no logueado o sin perfil)
    recomendados = []
    if tipo_piel:
        recomendados = list(
            Producto.objects.filter(tipo_piel__in=[tipo_piel, 'todos'])
        )

    return render(request, 'catalogo/catalogo.html', {
        'skincare':      skincare,
        'maquillaje':    maquillaje,
        'recomendados':  recomendados,
        'tipo_piel':     tipo_piel,
    })