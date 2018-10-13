from django.shortcuts import render , redirect
from apps.accounts.forms import SignUpForm
from django.contrib.auth.decorators import login_required
from apps.accounts.forms import *
from django.contrib import messages


def signup(request):
    # Usuario que hizo la peticion a la funcion (usuario que esta en la sesion)
    usuario = request.user
    # Validacion para cuando el administrador (is_staff)
    if usuario.is_staff:
        if request.method == 'POST':
            form = SignUpForm(request.POST)
            if form.is_valid():
                messages.success(request, 'Usuario registrado exitosamente')
                form.save()
                return render(request, 'accounts/signup.html', {'form': SignUpForm()})
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'accounts/signup.html', {'form': form})
        else:
            form = SignUpForm()
            return render(request, 'accounts/signup.html', {'form': form})
    # En caso de que el usuario no sea admin se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')


@login_required
def home(request):
    usuario = request.user
    if usuario.is_staff:
        return render(request, 'accounts/home.html', {'user': usuario})
    else:
        return render(request, 'accounts/home.html', {'user': usuario})
