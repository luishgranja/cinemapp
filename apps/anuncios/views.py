from django.shortcuts import render, redirect
from apps.anuncios.forms import *
from django.contrib import messages
from apps.anuncios.models import Anuncio
from apps.accounts.models import *


# Crear y consultar anuncios
def gestion_anuncios(request):
    usuario = request.user
    anuncios = Anuncio.objects.all()
    if usuario.is_staff:
        if request.method == 'POST':
            form = CrearAnuncioForm(request.POST, request.FILES)
            if form.is_valid:
                form.save()
                messages.success(request, 'Anuncio creado exitosamente')

                # Creacion de notificaciones sobre la promocion/anuncio
                usuarios = User.objects.filter(is_cliente=True)
                for usuario in usuarios:
                    Notificacion.objects.create(usuario=usuario,
                                                titulo=form.cleaned_data['nombre'],
                                                mensaje=str(form.cleaned_data['descripcion'])+' Válido desde: ' + str(form.cleaned_data['fecha_inicio']) + ' Hasta: ' + str(form.cleaned_data['fecha_final']),
                                                tipo=4)

                return render(request, 'anuncios/gestion_anuncios.html', {'form': CrearAnuncioForm(),
                                                                          'anuncios': anuncios})
            else:
                messages.success(request, 'Por favor corrige los errores')
                return render(request, 'anuncios/gestion_anuncios.html', {'form': form, 'anuncios': anuncios})

        else:
            form = CrearAnuncioForm()
            return render(request, 'anuncios/gestion_anuncios.html', {'form': form, 'anuncios': anuncios})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')


# Editar anuncio
def editar_anuncio(request, id_anuncio):
    usuario = request.user
    if usuario.is_staff:

        try:
            anuncio_editar = Anuncio.objects.get(id=id_anuncio)
        except Anuncio.DoesNotExist:
            messages.error(request, 'El anuncio solicitado no existe')
            return redirect('accounts:home')

        if request.method == 'POST':

            form = CrearAnuncioForm(request.POST, request.FILES, instance=anuncio_editar)
            if form.is_valid:
                form.save()
                messages.success(request, 'Anuncio modificado exitosamente')
                return redirect('anuncios:gestion_anuncios')
            else:
                messages.success(request, 'Por favor corrige los errores')
                return render(request, 'anuncios/editar_anuncio.html', {'form': form})
        else:
            form = CrearAnuncioForm(instance=anuncio_editar)
            return render(request, 'anuncios/editar_anuncio.html', {'form': form})
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')


# Ver anuncio
def ver_anuncio(request, id_anuncio):

    try:
        anuncio = Anuncio.objects.get(id=id_anuncio)
    except Anuncio.DoesNotExist:
        messages.error(request, 'El anuncio solicitado no existe')
        return redirect('accounts:home')

    if request.method == 'GET':
        return render(request, 'anuncios/ver_anuncio.html', {'anuncio': anuncio})


