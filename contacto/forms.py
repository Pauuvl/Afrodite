#Paulina Velasquez y Helen Sanabria
from django import forms
from django.utils.translation import gettext_lazy as _
from .models import MensajeContacto


class FormularioContacto(forms.ModelForm):
    class Meta:
        model = MensajeContacto
        fields = ['nombre', 'email', 'asunto', 'mensaje']
        widgets = {
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': _('Tu nombre completo'),
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'tu@email.com',
            }),
            'asunto': forms.Select(attrs={
                'class': 'form-select',
            }),
            'mensaje': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': _('¿En qué podemos ayudarte?'),
            }),
        }
        labels = {
            'nombre': _('Nombre'),
            'email': _('Correo electrónico'),
            'asunto': _('Asunto'),
            'mensaje': _('Mensaje'),
        }
