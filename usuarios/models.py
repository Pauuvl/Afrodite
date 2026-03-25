# Autores: Helen Sanabria 
from django.db import models
from django.contrib.auth.models import User

TIPO_PIEL_CHOICES = [
    ('normal', 'Normal'),
    ('seca', 'Seca'),
    ('grasa', 'Grasa'),
    ('mixta', 'Mixta'),
    ('sensible', 'Sensible'),
]

class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    documento_identidad = models.CharField(max_length=20, blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    tipo_piel = models.CharField(max_length=20, choices=TIPO_PIEL_CHOICES, blank=True, null=True)

    def __str__(self):
        return f'Perfil de {self.usuario.username}'


class DireccionUsuario(models.Model):
    perfil = models.ForeignKey(PerfilUsuario, on_delete=models.CASCADE, related_name='direcciones')
    es_predeterminada = models.BooleanField(default=False)
    nombre_destinatario = models.CharField(max_length=100, blank=True)
    direccion = models.CharField(max_length=200)
    info_adicional = models.CharField(max_length=200, blank=True, null=True)
    ciudad = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100, blank=True)
    pais = models.CharField(max_length=100, default='Colombia')
    telefono = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return f'{self.direccion}, {self.ciudad}'