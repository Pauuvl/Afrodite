# Autor: Paulina Velasquez Londoño
from django.urls import path
from . import views

urlpatterns = [
    path('catalogo/', views.catalogo, name='catalogo'),
    path('carrito/agregar/<int:producto_id>/', views.agregar_carrito, name='agregar_carrito'),
]