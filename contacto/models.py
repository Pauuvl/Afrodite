from django.db import models


class MensajeContacto(models.Model):
    ASUNTO_CHOICES = [
        ('pedido', 'Consulta sobre pedido'),
        ('producto', 'Información de producto'),
        ('devolucion', 'Devolución o cambio'),
        ('otro', 'Otro'),
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
        verbose_name = 'Mensaje de contacto'
        verbose_name_plural = 'Mensajes de contacto'
