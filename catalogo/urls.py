# Autor: Paulina Velasquez Londoño y Helen Sanabria
from django.urls import path
from . import views

urlpatterns = [
    path('catalogo/', views.catalogo, name='catalogo'),
<<<<<<< HEAD
]
=======
    path('api/productos/', views.api_productos, name='api_productos'),
]
>>>>>>> origin/main
