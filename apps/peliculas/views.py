from django.shortcuts import render, redirect
from .forms import *
from django.contrib import messages


def crearPelicula(request):
    # Usuario que hizo la peticion a la funcion (usuario que esta en la sesion)
    usuario = request.user
    # Validacion para cuando el administrador (is_staff)
    if True:
        if request.method == 'POST':
            form = CrearPeliculaForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Película registrada exitosamente')
                return render(request, 'peliculas/crear_peliculas.html', {'form': CrearPeliculaForm(), 'peliculas': listar_peliculas()})
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'peliculas/crear_peliculas.html', {'form': form, 'peliculas': listar_peliculas()})
        else:
            form = CrearPeliculaForm()
            return render(request, 'peliculas/crear_peliculas.html', {'form': form, 'peliculas': listar_peliculas()})

    # En caso de que el usuario no sea gerente se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')


def listar_peliculas():
    return Pelicula.get_peliculas()


def editar_pelicula(request, id_pelicula):
    usuario = request.user
    pelicula = Pelicula.objects.get(id=id_pelicula)

    if True:
        if request.method == 'POST':
            form = CrearPeliculaForm(request.POST, request.FILES, instance=pelicula)
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


def consultar_peliculas(request):
    return render(request,'peliculas/consultar_peliculas.html', {'peliculas': listar_peliculas()})


def listar_pelicula(slug):
    return Pelicula.get_pelicula(slug)


def ver_pelicula(request, slug):
    return render(request,'peliculas/consultar_pelicula.html',{'peli': listar_pelicula(slug)})


def listar_generos():
    return Genero.get_generos()


def crear_genero(request):
    usuario = request.user
    if request.method == 'POST':
        form = CrearGeneroForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Género creado exitosamente!')
            return render(request, 'peliculas/gestion_generos.html', {'form': CrearGeneroForm(), 'generos':listar_generos()})
        else:
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'peliculas/gestion_generos.html', {'form': form, 'generos':listar_generos()})
    else:
        form = CrearGeneroForm()
        return render(request, 'peliculas/gestion_generos.html', {'form': form, 'generos':listar_generos()})


