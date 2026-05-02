from django.urls import path
from . import views

app_name = 'panel_admin'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('pedidos/', views.pedidos, name='pedidos'),
    path('pedidos/<int:pk>/', views.pedido_detalle, name='pedido_detalle'),
    path('catalogo/', views.catalogo_lista, name='catalogo'),
    path('catalogo/nuevo/', views.producto_nuevo, name='producto_nuevo'),
    path('catalogo/<int:pk>/editar/', views.producto_editar, name='producto_editar'),
    path('catalogo/<int:pk>/eliminar/', views.producto_eliminar, name='producto_eliminar'),
    path('mensajes/', views.mensajes, name='mensajes'),
    path('mensajes/<int:pk>/', views.mensaje_detalle, name='mensaje_detalle'),
    path('mensajes/<int:pk>/eliminar/', views.mensaje_eliminar, name='mensaje_eliminar'),
]
