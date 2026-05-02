# Autores: Helen Sanabria
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import PerfilUsuario, DireccionUsuario

class FormularioRegistro(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'Correo electrónico'
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Nombre'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Apellido'
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.required = True  # todos obligatorios


class FormularioLogin(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
        # Sin field.required = True porque AuthenticationForm ya lo maneja


class FormularioPerfilUsuario(forms.ModelForm):
    first_name = forms.CharField(required=False, label='Nombre', widget=forms.TextInput(attrs={'class': 'form-control'}))
    last_name = forms.CharField(required=False, label='Apellido', widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=False, label='Correo electrónico', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = PerfilUsuario
        fields = ['documento_identidad', 'telefono', 'tipo_piel']
        labels = {
            'documento_identidad': 'Documento de identidad',
            'telefono': 'Teléfono',
            'tipo_piel': 'Tipo de piel',
        }
        widgets = {
            'documento_identidad': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo_piel': forms.Select(attrs={'class': 'form-select'}),
        }


class FormularioDireccion(forms.ModelForm):
    class Meta:
        model = DireccionUsuario
        fields = ['nombre_destinatario', 'direccion', 'info_adicional', 'ciudad', 'departamento', 'pais', 'telefono', 'es_predeterminada']
        labels = {
            'nombre_destinatario': 'Nombre completo',
            'direccion': 'Dirección',
            'info_adicional': 'Información adicional (apto, torre, etc.)',
            'ciudad': 'Ciudad',
            'departamento': 'Departamento',
            'pais': 'País',
            'telefono': 'Teléfono',
            'es_predeterminada': 'Establecer como dirección predeterminada',
        }
        widgets = {
            'nombre_destinatario': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'info_adicional': forms.TextInput(attrs={'class': 'form-control'}),
            'ciudad': forms.TextInput(attrs={'class': 'form-control'}),
            'departamento': forms.TextInput(attrs={'class': 'form-control'}),
            'pais': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'es_predeterminada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }