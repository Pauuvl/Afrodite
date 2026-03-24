# Autores: Helen Sanabria
from django.contrib import admin
from django.urls import path, include
from catalogo import views as catalogo_views
from django.conf import settings
from django.conf.urls.static import static

def index(request):
    from django.shortcuts import render
    return render(request, 'index.html')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('catalogo/', catalogo_views.catalogo, name='catalogo'),
    path('', include('usuarios.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
