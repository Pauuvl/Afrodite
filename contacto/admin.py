from django.contrib import admin
from .models import MensajeContacto


@admin.register(MensajeContacto)
class MensajeContactoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'asunto', 'leido', 'creado_en']
    list_filter = ['leido', 'asunto']
    search_fields = ['nombre', 'email', 'mensaje']
