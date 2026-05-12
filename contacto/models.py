#Paulina Velásquez y Helen Sanabria
from django.db import models
from django.utils.translation import gettext_lazy as _


class MensajeContacto(models.Model):
    ASUNTO_CHOICES = [
        ('pedido', _('Consulta sobre pedido')),
        ('producto', _('Información de producto')),
        ('devolucion', _('Devolución o cambio')),
        ('otro', _('Otro')),
    ]

    nombre = models.CharField(max_length=100)
    email = models.EmailField()
    asunto = models.CharField(max_length=20, choices=ASUNTO_CHOICES, default='otro')
    mensaje = models.TextField()
    leido = models.BooleanField(default=False)
    creado_en = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre} - {self.get_asunto_display()} ({self.creado_en.strftime('%d/%m/%Y')})"

    class Meta:
        ordering = ['-creado_en']
        verbose_name = _('Mensaje de contacto')
        verbose_name_plural = _('Mensajes de contacto')
