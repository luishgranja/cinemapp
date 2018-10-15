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
            form = createSurcursalForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Sucursal registrada exitosamente')
                form.save()
                return render(request, 'sucursales/crearSucursal.html', {'form': createSurcursalForm()})
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'sucursales/crearSucursal.html', {'form': form})
        else:
            form = createSurcursalForm()
            return render(request, 'sucursales/crearSucursal.html', {'form': form})

    # En caso de que el usuario no sea gerente se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')