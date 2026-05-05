def mensajes_sin_leer(request):
    """Inyecta el conteo de mensajes sin leer para el sidebar del panel admin."""
    if request.user.is_authenticated and request.user.is_staff:
        from contacto.models import MensajeContacto
        count = MensajeContacto.objects.filter(leido=False).count()
        return {'mensajes_sin_leer': count}
    return {'mensajes_sin_leer': 0}
