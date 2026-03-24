from django.db import models

class Producto(models.Model):
    CATEGORIAS = [
        ('skincare', 'Skincare'),
        ('maquillaje', 'Maquillaje'),
    ]

    nombre    = models.CharField(max_length=200)
    precio    = models.DecimalField(max_digits=10, decimal_places=0)
    categoria = models.CharField(max_length=20, choices=CATEGORIAS)
    imagen    = models.ImageField(upload_to='')  # ← sin subcarpeta

    def __str__(self):
        return self.nombre