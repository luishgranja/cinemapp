from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages
# Create your views here.
# Create your views here.
def crearPelicula(request):
    # Usuario que hizo la peticion a la funcion (usuario que esta en la sesion)
    usuario = request.user
    # Validacion para cuando el administrador (is_staff)
    if True:
        if request.method == 'POST':
            form = CrearPeliculaForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Película registrada exitosamente')
                form.save()
                return render(request, 'peliculas/crear_peliculas.html', {'form': CrearPeliculaForm()})
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'peliculas/crear_peliculas.html', {'form': form})
        else:
            form = CrearPeliculaForm()
            return render(request, 'peliculas/crear_peliculas.html', {'form': form})

    # En caso de que el usuario no sea gerente se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')


def listar_peliculas():
    return Pelicula.get_info()


def editar_pelicula(request, id_pelicula):
    usuario = request.user
    pelicula = Pelicula.objects.get(id=id_pelicula)

    if True:
        if request.method == 'POST':
            form = CrearPeliculaForm(request.POST, instance=pelicula)
            if form.is_valid():
                form.save()
                messages.success(request, 'Película modificada exitosamente!')
                return redirect('peliculas:crear')
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'peliculas/editar_pelicula.html', {'form': form})
        else:
            form = CrearPeliculaForm(instance=pelicula)
            return render(request, 'peliculas/editar_pelicula.html', {'form': form})

    # En caso de que el usuario no sea gerente se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')