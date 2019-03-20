from django.shortcuts import render
from .forms import *
from .models import *
# Create your views here.
def crear_funcion(request):
    # Usuario que hizo la peticion a la funcion (usuario que esta en la sesion)
    usuario = request.user
    # Validacion para cuando el administrador (is_staff)
    if usuario.is_staff or True:
        if request.method == 'POST':
            form = CrearFuncionForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Funcion registrada exitosamente')
                return render(request, 'funciones/crear_funcion.html', {'form': CrearFuncionForm(), 'funciones': listar_funciones()})
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'funciones/crear_funcion.html', {'form': form, 'funciones': listar_funciones()})
        else:
            form = CrearFuncionForm()
            return render(request, 'funciones/crear_funcion.html', {'form': form, 'funciones': listar_funciones()})

    # En caso de que el usuario no sea gerente se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')

def listar_funciones():
    return Funcion.get_funciones()