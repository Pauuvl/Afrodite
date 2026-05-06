# Autor: Paulina Velasquez Londoño
from django.db import models

TIPO_PIEL_CHOICES = [
    ('normal', 'Normal'),
    ('seca', 'Seca'),
    ('grasa', 'Grasa'),
    ('mixta', 'Mixta'),
    ('sensible', 'Sensible'),
]

class Producto(models.Model):
    CATEGORIAS = [
        ('skincare', 'Skincare'),
        ('maquillaje', 'Maquillaje'),
    ]

    TIPO_PIEL_PRODUCTO = [
        ('todos', 'Todos'),
        ('normal', 'Normal'),
        ('seca', 'Seca'),
        ('grasa', 'Grasa'),
        ('mixta', 'Mixta'),
        ('sensible', 'Sensible'),
    ]

    nombre     = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, default='')
    precio     = models.DecimalField(max_digits=10, decimal_places=0)
    categoria  = models.CharField(max_length=20, choices=CATEGORIAS)
    imagen     = models.ImageField(upload_to='')
    tipo_piel  = models.CharField(
        max_length=20,
        choices=TIPO_PIEL_PRODUCTO,
        default='todos'
    )
    stock = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.nombre

    @property
    def agotado(self):
        return self.stock == 0
