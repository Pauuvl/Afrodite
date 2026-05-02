from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.db.models import Sum, Count
from catalogo.models import Producto
from carrito.models import Order, OrderItem
from contacto.models import MensajeContacto
from .forms import ProductoForm


def admin_required(view_func):
    """Decorator: requiere is_staff."""
    from functools import wraps
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            from django.shortcuts import redirect
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return _wrapped


# ── DASHBOARD ─────────────────────────────────────────────────
@admin_required
def dashboard(request):
    total_pedidos = Order.objects.count()
    ingresos = Order.objects.filter(status='paid').aggregate(total=Sum('total'))['total'] or 0
    total_productos = Producto.objects.count()
    agotados = Producto.objects.filter(stock=0).count()
    mensajes_nuevos = MensajeContacto.objects.filter(leido=False).count()
    pedidos_recientes = Order.objects.select_related('user').order_by('-created_at')[:5]

    return render(request, 'panel_admin/dashboard.html', {
        'total_pedidos': total_pedidos,
        'ingresos': ingresos,
        'total_productos': total_productos,
        'agotados': agotados,
        'mensajes_nuevos': mensajes_nuevos,
        'pedidos_recientes': pedidos_recientes,
    })


# ── PEDIDOS ───────────────────────────────────────────────────
@admin_required
def pedidos(request):
    estado = request.GET.get('estado', '')
    qs = Order.objects.select_related('user').prefetch_related('orderitem_set__product').order_by('-created_at')
    if estado:
        qs = qs.filter(status=estado)
    return render(request, 'panel_admin/pedidos.html', {
        'pedidos': qs,
        'estado_filtro': estado,
    })


@admin_required
def pedido_detalle(request, pk):
    order = get_object_or_404(Order, pk=pk)
    items = order.orderitem_set.select_related('product').all()
    if request.method == 'POST':
        nuevo_estado = request.POST.get('status')
        if nuevo_estado in dict(Order.STATUS_CHOICES):
            order.status = nuevo_estado
            order.save()
            messages.success(request, 'Estado del pedido actualizado.')
        return redirect('panel_admin:pedido_detalle', pk=pk)
    return render(request, 'panel_admin/pedido_detalle.html', {
        'order': order,
        'items': items,
    })


# ── CATÁLOGO ──────────────────────────────────────────────────
@admin_required
def catalogo_lista(request):
    productos = Producto.objects.all().order_by('categoria', 'nombre')
    return render(request, 'panel_admin/catalogo.html', {'productos': productos})


@admin_required
def producto_nuevo(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto creado correctamente.')
            return redirect('panel_admin:catalogo')
    else:
        form = ProductoForm()
    return render(request, 'panel_admin/producto_form.html', {
        'form': form, 'titulo': 'Nuevo producto', 'accion': 'Crear'
    })


@admin_required
def producto_editar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Producto actualizado.')
            return redirect('panel_admin:catalogo')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'panel_admin/producto_form.html', {
        'form': form, 'titulo': f'Editar: {producto.nombre}', 'accion': 'Guardar cambios'
    })


@admin_required
def producto_eliminar(request, pk):
    producto = get_object_or_404(Producto, pk=pk)
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'"{nombre}" eliminado.')
        return redirect('panel_admin:catalogo')
    return render(request, 'panel_admin/producto_confirmar_eliminar.html', {'producto': producto})


# ── MENSAJES DE CONTACTO ──────────────────────────────────────
@admin_required
def mensajes(request):
    solo_nuevos = request.GET.get('nuevos', '')
    qs = MensajeContacto.objects.all()
    if solo_nuevos:
        qs = qs.filter(leido=False)
    return render(request, 'panel_admin/mensajes.html', {
        'mensajes': qs,
        'solo_nuevos': bool(solo_nuevos),
    })


@admin_required
def mensaje_detalle(request, pk):
    msg = get_object_or_404(MensajeContacto, pk=pk)
    if not msg.leido:
        msg.leido = True
        msg.save()
    return render(request, 'panel_admin/mensaje_detalle.html', {'msg': msg})


@admin_required
def mensaje_eliminar(request, pk):
    msg = get_object_or_404(MensajeContacto, pk=pk)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, 'Mensaje eliminado.')
        return redirect('panel_admin:mensajes')
    return redirect('panel_admin:mensajes')
