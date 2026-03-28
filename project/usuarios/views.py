from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Usuario
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import update_session_auth_hash
import os

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('core:index')
        else:
            return render(request, 'usuarios/login.html', {'error': 'Usuario o contraseña incorrectos'})

    return render(request, 'usuarios/login.html')


def registro_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['confirm_password']
        nombre = request.POST['nombre']
        apellido = request.POST['apellido']
        dni = request.POST['dni']
        email = request.POST['email']
        telefono = request.POST['telefono']
        foto = request.FILES.get('foto')
        tipo_usuario = 'alumno'

        if Usuario.objects.filter(username=username).exists():
            return render(request, 'usuarios/registro.html', {
                'error': 'El usuario ya existe'
            })

        user = Usuario.objects.create_user(
            username=username,
            password=password,
            first_name=nombre,
            last_name=apellido,
            dni=dni,
            email=email,
            telefono=telefono,
            foto=foto,
            tipo_usuario=tipo_usuario
        )

        login(request, user)
        return redirect('core:index')

    return render(request, 'usuarios/registro.html')


def logout_view(request):
    logout(request)
    return redirect('usuarios:login')

@login_required
def perfil_view(request):
    return render(request, 'usuarios/perfil.html', {'usuario': request.user})

@login_required
def editar_perfil(request):
    user = request.user

    if request.method == 'POST':
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.dni = request.POST.get('dni')
        user.telefono = request.POST.get('telefono')
        password_actual = request.POST.get('password_actual')
        password = request.POST.get('password')

        if password:
            if check_password(password_actual, user.password):
                user.password = make_password(password)
            else:
                return render(request, 'usuarios/editar-perfil.html', {'usuario': user, 'error': 'Contraseña actual incorrecta'})

        if request.FILES.get('foto'):
            if user.foto:
                if os.path.isfile(user.foto.path):
                    os.remove(user.foto.path)
            user.foto = request.FILES.get('foto')

        user.save()
        update_session_auth_hash(request, user)
        return redirect('usuarios:perfil')

    return render(request, 'usuarios/editar-perfil.html', {'usuario': user})
