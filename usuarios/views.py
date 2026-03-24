# Autores: Helen Sanabria
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from .forms import FormularioRegistro, FormularioLogin, FormularioPerfilUsuario, FormularioDireccion
from .models import PerfilUsuario, DireccionUsuario


def vista_registro(request):
    if request.user.is_authenticated:
        return redirect('perfil')
    if request.method == 'POST':
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            PerfilUsuario.objects.create(usuario=user)
            login(request, user)
            messages.success(request, f'¡Bienvenida, {user.first_name}!')
            return redirect('index')
    else:
        form = FormularioRegistro()
    return render(request, 'usuarios/registro.html', {'form': form})


def vista_login(request):
    if request.user.is_authenticated:
        return redirect('perfil')
    if request.method == 'POST':
        form = FormularioLogin(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'¡Hola, {user.first_name or user.username}!')
            return redirect('index')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    else:
        form = FormularioLogin()
    return render(request, 'usuarios/login.html', {'form': form})


def vista_logout(request):
    logout(request)
    return redirect('index')


@login_required
def vista_perfil(request):
    perfil, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    direcciones = perfil.direcciones.all()

    if request.method == 'POST':
        form = FormularioPerfilUsuario(request.POST, instance=perfil)
        if form.is_valid():
            request.user.first_name = form.cleaned_data.get('first_name', '')
            request.user.last_name = form.cleaned_data.get('last_name', '')
            request.user.email = form.cleaned_data.get('email', '')
            request.user.save()
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')
    else:
        form = FormularioPerfilUsuario(instance=perfil, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    return render(request, 'usuarios/perfil.html', {
        'form': form,
        'perfil': perfil,
        'direcciones': direcciones,
    })


@login_required
def agregar_direccion(request):
    perfil, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    if request.method == 'POST':
        form = FormularioDireccion(request.POST)
        if form.is_valid():
            direccion = form.save(commit=False)
            direccion.perfil = perfil
            if direccion.es_predeterminada:
                perfil.direcciones.update(es_predeterminada=False)
            direccion.save()
            messages.success(request, 'Dirección agregada.')
            return redirect('perfil')
    else:
        form = FormularioDireccion()
    return render(request, 'usuarios/direccion_form.html', {'form': form, 'accion': 'Agregar'})


@login_required
def editar_direccion(request, pk):
    perfil, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    direccion = get_object_or_404(DireccionUsuario, pk=pk, perfil=perfil)
    if request.method == 'POST':
        form = FormularioDireccion(request.POST, instance=direccion)
        if form.is_valid():
            if form.cleaned_data.get('es_predeterminada'):
                perfil.direcciones.update(es_predeterminada=False)
            form.save()
            messages.success(request, 'Dirección actualizada.')
            return redirect('perfil')
    else:
        form = FormularioDireccion(instance=direccion)
    return render(request, 'usuarios/direccion_form.html', {'form': form, 'accion': 'Editar'})


@login_required
def eliminar_direccion(request, pk):
    perfil, _ = PerfilUsuario.objects.get_or_create(usuario=request.user)
    direccion = get_object_or_404(DireccionUsuario, pk=pk, perfil=perfil)
    direccion.delete()
    messages.success(request, 'Dirección eliminada.')
    return redirect('perfil')