from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from .models import Ejercicio, DiaRutina

@login_required
def rutinas(request):
    user = request.user
    return render(request, 'rutinas/rutinas.html', {'usuario': user})

@login_required
def crear_rutina(request):
    ejercicios = Ejercicio.objects.all()
    user = request.user
    usuarios = Usuario.objects.all()
    return render(request, 'rutinas/crear-rutina.html', {'usuario': user, 'usuarios': usuarios, 'ejercicios': ejercicios})

@login_required
def cargar_ejercicio(request):
    ejercicios = Ejercicio.objects.all()
    return render(request, 'rutinas/cargar-ejercicio.html', {'ejercicios': ejercicios})

@login_required
def centro_rutinas(request):
    user = request.user
    return render(request, 'rutinas/centro-rutinas.html', {'usuario': user})