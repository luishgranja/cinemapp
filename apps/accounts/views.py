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
            user_data = FormEmpleado(request.POST)
            if form.is_valid() and user_data.is_valid():
                messages.success(request, 'Empleado registrado exitosamente')

                user = form.save(commit=False)
                user.save()

                user_extra = user_data.save(commit=False)
                user_extra.user = user
                user_extra.save()

                return render(request, 'accounts/signup.html', {'form': SignUpForm(), 'form_empleado': FormEmpleado()})
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'accounts/signup.html', {'form': form, 'form_empleado': user_data})
        else:
            form = SignUpForm()
            form_empleado = FormEmpleado()
            return render(request, 'accounts/signup.html', {'form': form, 'form_empleado': form_empleado, 'empleados': listar_empleados()})
    # En caso de que el usuario no sea admin se redirije al home y se muestra mensaje de error
    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')


def signup_cliente(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        user_data = FormCliente(request.POST)
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
        user_data = FormCliente()
        return render(request, 'accounts/signup_cliente.html', {'form': form, 'user_form': user_data})


@login_required
def home(request):
    usuario = request.user
    if usuario.is_staff:
        return render(request, 'accounts/home.html', {'user': usuario})
    else:
        return render(request, 'accounts/home.html', {'user': usuario})


def listar_empleados():
    return Empleado.get_info()


def editar_empleado(request, idUser):
    empleado = Empleado.objects.get(id=idUser)
    user = User.objects.get(id=empleado.user.id)
    usuario = request.user

    if True:

        if request.method == 'POST':

            form = EditUserForm(request.POST, instance=user)
            form_empleado = FormEmpleado(request.POST, instance=empleado)
            if form.is_valid() and form_empleado.is_valid():
                form.save()
                form_empleado.save()
                messages.success(request, 'Has modificado el empleado exitosamente!')
                return redirect('accounts:registro')
            else:
                messages.error(request, 'Por favor corrige los errores')
                return render(request, 'accounts/editar_empleado.html', {'form': form, 'form_empleado':form_empleado})

        else:
            form = EditUserForm(instance=user)
            form_empleado = FormEmpleado(instance=empleado)
            return render(request, 'accounts/editar_empleado.html', {'form': form, 'form_empleado':form_empleado})

    else:
        messages.error(request, 'No estas autorizado para realizar esta acción')
        return redirect('accounts:home')











