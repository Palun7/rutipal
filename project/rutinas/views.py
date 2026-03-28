from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from .models import Ejercicio, DiaRutina, RutinaEjercicio
from collections import defaultdict

@login_required
def rutinas(request):
    usuario = request.user
    rutinas = DiaRutina.objects.filter(usuario=request.user).prefetch_related('ejercicio')

    rutinas_por_mes = defaultdict(list)

    for rutina in rutinas:
        rutinas_por_mes[rutina.mes].append(rutina)

    return render(request, 'rutinas/rutinas.html', {
        'usuario': usuario,
        'rutinas_por_mes': dict(rutinas_por_mes)
    })

@login_required
def crear_rutina(request):
    ejercicios = Ejercicio.objects.all()
    user = request.user
    usuarios = Usuario.objects.all()

    if request.method == 'POST':
        usuario_id = request.POST['usuario']
        usuario = Usuario.objects.get(id=usuario_id)

        mes = request.POST['mes']
        dia = request.POST['dia']
        ejercicio_ids = request.POST.getlist('ejercicio')

        rutina = DiaRutina.objects.create(
            usuario=usuario,
            mes=mes,
            dia=dia
        )

        for ejercicio_id in ejercicio_ids:
            RutinaEjercicio.objects.create(
                rutina=rutina,
                ejercicio_id=ejercicio_id,
                peso=request.POST.get(f'peso_{ejercicio_id}'),
                repeticiones=request.POST.get(f'reps_{ejercicio_id}'),
                series=request.POST.get(f'series_{ejercicio_id}')
            )

        rutina.ejercicio.set(ejercicio_ids)
        rutina.save()

    return render(request, 'rutinas/crear-rutina.html', {
        'usuario': user,
        'usuarios': usuarios,
        'ejercicios': ejercicios
    })

@login_required
def cargar_ejercicio(request):
    ejercicios = Ejercicio.objects.all()

    if request.method == 'POST':
        nombre = request.POST['nombre']
        musculo = request.POST['musculo']
        descripcion = request.POST['descripcion']
        imagen = request.FILES.get('imagen')
        url = request.POST.get('url')

        Ejercicio.objects.create(
            nombre=nombre,
            musculo=musculo,
            descripcion=descripcion,
            imagen=imagen,
            url=url
        )
    return render(request, 'rutinas/cargar-ejercicio.html', {'ejercicios': ejercicios})

@login_required
def centro_rutinas(request):
    user = request.user
    return render(request, 'rutinas/centro-rutinas.html', {'usuario': user})