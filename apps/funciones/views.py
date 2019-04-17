from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib import messages


def crear_funcion(request):
    # Usuario que hizo la peticion a la funcion (usuario que esta en la sesion)
    usuario = request.user

    try:
        empleado = Empleado.objects.get(user=usuario)
        cargo = empleado.cargo

    except Empleado.DoesNotExist:
        cargo = ''

    if usuario.is_staff:
        funciones = listar_funciones()
    else:
        funciones = listar_funciones_sucursal(usuario)

    # Validacion para cuando el administrador (is_staff)
    if usuario.is_staff or cargo == 'Gerente':
        if request.method == 'POST':
            form = CrearFuncionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Funcion registrada exitosamente')
                form_extra = CrearFuncionForm()
                form_extra.listarSalas(Empleado.objects.get(user=request.user).sucursal.id)
                return render(request, 'funciones/crear_funcion.html', {'form': form_extra,
                                                                        'funciones': funciones})
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'funciones/crear_funcion.html', {'form': form, 'funciones': funciones})
        else:
            form = CrearFuncionForm()
            form.listarSalas(Empleado.objects.get(user=request.user).sucursal.id)
            return render(request, 'funciones/crear_funcion.html', {'form': form, 'funciones': funciones})

    # En caso de que el usuario no sea gerente se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')


def editar_funcion(request, id_funcion):
    usuario = request.user
    funcion = Funcion.objects.get(id=id_funcion)

    if True:
        if request.method == 'POST':
            form = CrearFuncionForm(request.POST, instance=funcion)
            if form.is_valid():
                form.save()
                form_extra = CrearFuncionForm()
                form_extra.listarSalas(Empleado.objects.get(user=request.user).sucursal.id)
                messages.success(request, 'Función modificada exitosamente!')
                return redirect('funciones:crear')
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'funciones/editar_funcion.html', {'form': form})
        else:
            form = CrearFuncionForm(instance=funcion)
            return render(request, 'funciones/editar_funcion.html', {'form': form})

    # En caso de que el usuario no sea gerente se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')


def listar_funciones():
    return Funcion.get_funciones()


def listar_funciones_sucursal(usuario):
    return Funcion.get_funciones_sucursales(usuario)
