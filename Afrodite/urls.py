from django.contrib import admin
from django.urls import path, include
from . import views
from catalogo import views as catalogo_views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', catalogo_views.index, name='index'),
    path('catalogo/', catalogo_views.catalogo, name='catalogo'),
    path('carrito/', include('carrito.urls')),
    path('', include('usuarios.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
