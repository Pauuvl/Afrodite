# Autor: Viviana Arango Tabares y Helen Sanabria
from django.urls import path
from . import views

app_name = 'carrito'

urlpatterns = [
    path('',                        views.cart_detail, name='cart_detail'),
    path('agregar/',                views.agregar_producto, name='agregar_producto'),
    path('actualizar/<int:item_id>/', views.update_cart_item, name='actualizar_item'),
    path('eliminar/<int:item_id>/', views.remove_cart_item,    name='eliminar_item'),
    path('checkout/',               views.checkout,         name='checkout'),
    path('pago_exitoso/<int:order_id>/', views.pago_exitoso, name='payment_success'),
]
