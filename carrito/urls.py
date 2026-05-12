# Autor: Viviana Arango Tabares y Helen Sanabria
from django.urls import path
from . import views

app_name = 'carrito'

urlpatterns = [
    path('',                        views.detalle_carrito, name='detalle_carrito'),
    path('agregar/',                views.agregar_producto, name='agregar_producto'),
    path('actualizar/<int:item_id>/', views.actualizar_item, name='actualizar_item'),
    path('eliminar/<int:item_id>/', views.eliminar_item,    name='eliminar_item'),
    path('checkout/',               views.checkout,         name='checkout'),
    path('pago-exitoso/',           views.pago_exitoso,     name='pago_exitoso'),
]