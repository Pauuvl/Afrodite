# Autores: Helen Sanabria 
from django.urls import path
from . import views

urlpatterns = [
    path('registro/', views.vista_registro, name='registro'),
    path('login/', views.vista_login, name='login'),
    path('logout/', views.vista_logout, name='logout'),
    path('perfil/', views.vista_perfil, name='perfil'),
    path('perfil/direccion/agregar/', views.agregar_direccion, name='agregar_direccion'),
    path('perfil/direccion/editar/<int:pk>/', views.editar_direccion, name='editar_direccion'),
    path('perfil/direccion/eliminar/<int:pk>/', views.eliminar_direccion, name='eliminar_direccion'),
]