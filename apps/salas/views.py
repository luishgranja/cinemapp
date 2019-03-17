from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages
from django.http import HttpResponse
import json


def crear_sala(request):
    # Usuario que hizo la peticion a la funcion (usuario que esta en la sesion)
    usuario = request.user
    # Validacion para cuando el administrador (is_staff)
    if True:
        if request.method == 'POST':
            form = CrearSalaForm(request.POST)
            lista_sillas=request.POST.getlist('silla')
            if form.is_valid():
                inst = form.save()
                for silla in lista_sillas:
                    silla = json.loads(silla)
                    silla_aux=Silla()
                    silla_aux.nombre="a1"
                    silla_aux.sala=inst
                    silla_aux.ubicacion_x=int(silla["i"])
                    silla_aux.ubicacion_y=int(silla["j"])
                    if silla["color"] == Silla.SIN_MARCAR:
                        silla_aux.tipo=Silla.SIN_MARCAR
                    elif silla["color"] == Silla.GENERAL:
                        silla_aux.tipo=Silla.GENERAL
                    elif silla["color"] == Silla.DISCAPACITADO:
                        silla_aux.tipo=Silla.DISCAPACITADO
                    elif silla["color"] == Silla.PREFERENCIAL:
                        silla_aux.tipo=Silla.PREFERENCIAL
                    silla_aux.save()
                messages.success(request, 'Sala registrada exitosamente')
                return render(request, 'salas/crear_salas.html', {'form': CrearSalaForm(),'salas': listar_salas(),'itemlist': list(range(0,30))})
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'salas/crear_salas.html', {'form': form, 'salas': listar_salas(),'itemlist': list(range(0,30))})
        else:
            form = CrearSalaForm()
            return render(request, 'salas/crear_salas.html', {'form': form,'salas': listar_salas(),'itemlist': list(range(0,30))})

    # En caso de que el usuario no sea gerente se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')

def listar_salas():
    return Sala.get_salas()

def listar_sala(id):
    return Sala.get_sala(id)

def editar_sala(request, id_sala):
    usuario = request.user
    sala = Sala.objects.get(id=id_sala)
    sillas=sala.sillas.all()
    print(sillas[0].tipo)

    if True:
        if request.method == 'POST':
            form = CrearSalaForm(request.POST, instance=sala)
            if form.is_valid():
                for silla in sillas:
                    silla.delete()
            lista_sillas=request.POST.getlist('silla')
            print(lista_sillas)
            if form.is_valid():
                inst = form.save()
                for silla in lista_sillas:
                    silla = json.loads(silla)
                    silla_aux=Silla()
                    silla_aux.nombre="a1"
                    silla_aux.sala=inst
                    silla_aux.ubicacion_x=int(silla["i"])
                    silla_aux.ubicacion_y=int(silla["j"])
                    if silla["color"] == Silla.SIN_MARCAR:
                        silla_aux.tipo=Silla.SIN_MARCAR
                    elif silla["color"] == Silla.GENERAL:
                        silla_aux.tipo=Silla.GENERAL
                    elif silla["color"] == Silla.DISCAPACITADO:
                        silla_aux.tipo=Silla.DISCAPACITADO
                    elif silla["color"] == Silla.PREFERENCIAL:
                        silla_aux.tipo=Silla.PREFERENCIAL
                    silla_aux.save()
                messages.success(request, 'Sala modificada exitosamente!')
                return redirect('salas:crear')
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'salas/crear_salas.html', {'form': form})
        else:

            lista_sillas=[]
            for i in range(0,901):
                lista_sillas.append(False)

            for silla in sillas:
                silla_numero=(30*(silla.ubicacion_x+1-1))+silla.ubicacion_y+1
                lista_sillas[silla_numero]=silla
            form = CrearSalaForm(instance=sala)
            return render(request, 'salas/editar_sala.html', {'form': form,'itemlist': list(range(0,30)),'lista_sillas': lista_sillas})
    # En caso de que el usuario no sea gerente se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')

def ver_sala(request,id_sala):

    sala= Sala.objects.get(id=id_sala)
    sillas=sala.sillas.all()
    lista_sillas=[]
    for i in range(0,901):
        lista_sillas.append(False)

    for silla in sillas:
        silla_numero=(30*(silla.ubicacion_x-1))+silla.ubicacion_y
        lista_sillas[silla_numero]=True

    return render(request, 'salas/consultar_sala.html', {'sala': listar_sala(id_sala),'itemlist': list(range(0,30)),'lista_sillas': lista_sillas})



    
