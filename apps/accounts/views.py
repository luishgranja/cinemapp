from django.shortcuts import render , redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from apps.accounts.forms import *
from django.contrib import messages


def signup(request):
    # Usuario que hizo la peticion a la funcion (usuario que esta en la sesion)
    usuario = request.user
    # Validacion para cuando el administrador (is_staff)
    if True:
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


def signup_cliente(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        user_data = SignUpFormCliente(request.POST)
        if form.is_valid() and user_data.is_valid():

            user = form.save(commit=False)
            user.is_cliente = True
            user.save()

            user_extra = user_data.save(commit=False)
            user_extra.user = user
            user_extra.save()

            # login(request, request.user)
            return redirect('accounts:login')
        else:
            messages.error(request, 'Por favor corrige los errores')
            return render(request, 'accounts/signup_cliente.html', {'form': form, 'user_form': user_data})
    else:
        form = SignUpForm()
        user_data = SignUpFormCliente()
        return render(request, 'accounts/signup_cliente.html', {'form': form, 'user_form': user_data})


@login_required
def home(request):
    usuario = request.user
    if usuario.is_staff:
        return render(request, 'accounts/home.html', {'user': usuario})
    else:
        return render(request, 'accounts/home.html', {'user': usuario})
