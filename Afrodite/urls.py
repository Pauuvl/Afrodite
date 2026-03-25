# Autor: Todos
from django.contrib import admin
from django.urls import path, include
from catalogo import views as catalogo_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', catalogo_views.index, name='index'),
    path('catalogo/', catalogo_views.catalogo, name='catalogo'),

    path('carrito/agregar/<int:producto_id>/', catalogo_views.agregar_carrito, name='agregar_carrito'),

    path('carrito/', include('carrito.urls')),

    # usuarios sin prefijo → /perfil/, /login/, /registro/, /logout/ accesibles desde raíz
    path('', include('usuarios.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)