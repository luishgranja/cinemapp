from django.shortcuts import render, redirect
from apps.sucursales.forms import *
from django.contrib import messages

# Create your views here.
def createSucursal(request):
    # Usuario que hizo la peticion a la funcion (usuario que esta en la sesion)
    usuario = request.user
    # Validacion para cuando el administrador (is_staff)
    if True:
        if request.method == 'POST':
            form = CreateSurcursalForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Sucursal registrada exitosamente')
                form.save()
                return render(request, 'sucursales/crearSucursal.html', {'form': CreateSurcursalForm(), 'sucursales': listar_sucursales()})
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'sucursales/crearSucursal.html', {'form': form})
        else:
            form = CreateSurcursalForm()
            return render(request, 'sucursales/crearSucursal.html', {'form': form, 'sucursales': listar_sucursales()})

    # En caso de que el usuario no sea gerente se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')


def listar_sucursales():
    return Sucursal.get_info()


def editar_sucursal(request, id_sucursal):
    usuario = request.user
    sucursal = Sucursal.objects.get(id=id_sucursal)

    if True:
        if request.method == 'POST':
            form = EditarSucursalForm(request.POST, instance=sucursal)
            if form.is_valid():
                id_gerente = form.cleaned_data['gerente']
                if not(id_gerente == ''):
                    Empleado.objects.filter(id=id_gerente).update(sucursal_id=id_sucursal)
                form.save()
                messages.success(request, 'Sucursal modificada exitosamente!')
                return redirect('sucursales:crear')
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'sucursales/editar_sucursal.html', {'form': form})
        else:
            form = EditarSucursalForm(instance=sucursal)
            return render(request, 'sucursales/editar_sucursal.html', {'form': form})

    # En caso de que el usuario no sea gerente se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')
