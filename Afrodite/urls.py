# Autor: Todos
from django.contrib import admin
from django.urls import path, include
from catalogo import views as catalogo_views
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', catalogo_views.index, name='index'),
    path('catalogo/', catalogo_views.catalogo, name='catalogo'),
    path('i18n/', include('django.conf.urls.i18n')),
    path('carrito/', include('carrito.urls')),
    path('contacto/', include('contacto.urls')),
    path('mi-panel/', include('panel_admin.urls')),
    # usuarios sin prefijo → /perfil/, /login/, /registro/, /logout/ accesibles desde raíz
    path('', include('usuarios.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

