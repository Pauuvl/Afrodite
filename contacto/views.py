from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import FormularioContacto


def contacto(request):
    if request.method == 'POST':
        form = FormularioContacto(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Mensaje enviado! Te responderemos pronto.')
            return redirect('contacto')
    else:
        form = FormularioContacto()
    return render(request, 'contacto/contacto.html', {'form': form})
