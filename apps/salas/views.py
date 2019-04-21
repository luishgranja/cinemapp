import json

import numpy as np
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import *
from .models import *


def crear_sala(request):
    # Usuario que hizo la peticion a la funcion (usuario que esta en la sesion)
    usuario = request.user
    # Validacion para cuando el administrador (is_staff)

    try:
        empleado = Empleado.objects.get(user=usuario)
        cargo = empleado.cargo

    except Empleado.DoesNotExist:
        cargo = ''

    if usuario.is_staff:
        salas = listar_salas()
    else:
        salas = salas_de_sucursal(empleado.sucursal.id)

    if usuario.is_staff or cargo == 'Gerente':
        if request.method == 'POST':
            form = CrearSalaForm(request.POST)
            lista_sillas = request.POST.getlist('silla')
            if form.is_valid():
                inst = form.save()
                proceso_sillas(lista_sillas, inst)
                messages.success(request, 'Sala registrada exitosamente')
                return redirect('salas:crear')
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'salas/crear_salas.html', {'form': form, 'salas': salas,
                                                                  'itemlist': list(range(0, 26))})
        else:
            form = CrearSalaForm()
            if cargo == 'Gerente':
                form.fields['sucursal'].initial = empleado.sucursal
            return render(request, 'salas/crear_salas.html', {'form': form,
                                                              'salas': salas,
                                                              'itemlist': list(range(0, 26))})

    # En caso de que el usuario no sea gerente se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')


def listar_salas():
    return Sala.get_salas()


def salas_de_sucursal(id_sucursal):
    return Sala.get_salas_de_sucursal(id_sucursal)


def listar_sala(id_sala):
    return Sala.get_sala(id_sala)


def editar_sala(request, id_sala):
    usuario = request.user
    sala = Sala.objects.get(id=id_sala)
    sillas = sala.sillas.all()

    if True:
        if request.method == 'POST':
            form = CrearSalaForm(request.POST, instance=sala)
            if form.is_valid():
                for silla in sillas:
                    silla.delete()
            lista_sillas = request.POST.getlist('silla')
            if form.is_valid():
                inst = form.save()
                proceso_sillas(lista_sillas, inst)
                messages.success(request, 'Sala modificada exitosamente!')
                return redirect('salas:crear')
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'salas/crear_salas.html', {'form': form})
        else:

            lista_sillas = []
            for i in range(0, 677):
                lista_sillas.append(False)

            for silla in sillas:
                silla_numero = (26*(silla.ubicacion_x+1-1))+silla.ubicacion_y+1
                lista_sillas[silla_numero] = silla
            form = CrearSalaForm(instance=sala)
            return render(request, 'salas/editar_sala.html', {'form': form, 'itemlist': list(range(0, 26)),
                                                              'lista_sillas': lista_sillas})
    # En caso de que el usuario no sea gerente se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')


def ver_sala(request, id_sala):
    sala = Sala.objects.get(id=id_sala)
    sillas = sala.sillas.all()
    lista_sillas = []
    for i in range(0, 677):
        lista_sillas.append(False)                

    for silla in sillas:
        silla_numero = (26*(silla.ubicacion_x+1-1))+silla.ubicacion_y+1
        lista_sillas[silla_numero] = silla

    return render(request, 'salas/consultar_sala.html', {'sala': listar_sala(id_sala), 'itemlist': list(range(0, 26)),
                                                         'lista_sillas': lista_sillas})


def proceso_sillas(lista_sillas, inst):
    mi = np.full((26, 26), "...")
    for silla in lista_sillas:
        silla = json.loads(silla)
        silla_aux = Silla()
        silla_aux.sala = inst
        silla_aux.ubicacion_x = int(silla["i"])
        silla_aux.ubicacion_y = int(silla["j"])
        mi[silla_aux.ubicacion_x][silla_aux.ubicacion_y] = "---"
    a = 65
    b = 25
    cont = 0
    for i in range(0, 26):
        for j in reversed(range(0, 26)):
            if mi[i][j] == "---":
                    aux = str(chr(a))
                    aux += str(26-b)
                    b = b-1
                    cont = 1
                    mi[i][j] = aux
        b = 25
        if cont == 1:
            a = a+1
            cont = 0

    for silla in lista_sillas:
        silla = json.loads(silla)
        silla_aux = Silla()
        silla_aux.sala = inst
        silla_aux.ubicacion_x = int(silla["i"])
        silla_aux.ubicacion_y = int(silla["j"])
        silla_aux.nombre = mi[silla_aux.ubicacion_x][silla_aux.ubicacion_y]
                
        if silla["color"] == Silla.GENERAL:
            silla_aux.tipo = Silla.GENERAL
        elif silla["color"] == Silla.DISCAPACITADO:
            silla_aux.tipo = Silla.DISCAPACITADO
        elif silla["color"] == Silla.PREFERENCIAL:
            silla_aux.tipo = Silla.PREFERENCIAL
        silla_aux.save()
