from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from usuarios.models import Usuario
from .models import Ejercicio, DiaRutina, RutinaEjercicio
from collections import defaultdict
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json


@login_required
def rutinas(request):
    usuario = request.user

    rutinas = DiaRutina.objects.filter(usuario=usuario)\
        .prefetch_related('ejercicios__ejercicio')\
        .order_by('mes', 'dia')

    if request.method == 'POST':
        for rutina in rutinas:
            for r in rutina.ejercicios.all(): # type: ignore

                reps = request.POST.get(f'reps_{r.id}')
                series = request.POST.get(f'series_{r.id}')
                peso_raw = request.POST.get(f'peso_{r.id}')

                try:
                    peso = float(peso_raw) if peso_raw else None
                except ValueError:
                    peso = None

                r.peso = peso or None
                r.repeticiones = reps or None
                r.series = series or None
                r.save()

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
        usuario = get_object_or_404(Usuario, id=usuario_id)

        mes = request.POST['mes']
        dia = request.POST['dia']
        ejercicio_ids = request.POST.getlist('ejercicio')

        if not ejercicio_ids:
            return render(request, 'rutinas/crear-rutina.html', {
                'error': 'Debes seleccionar al menos un ejercicio',
                'usuarios': usuarios,
                'ejercicios': ejercicios
            })

        rutina, creada = DiaRutina.objects.get_or_create(
            usuario=usuario,
            mes=mes,
            dia=dia
        )

        for ejercicio_id in ejercicio_ids:
            peso = request.POST.get(f'peso_{ejercicio_id}') or None
            reps = request.POST.get(f'reps_{ejercicio_id}') or None
            series = request.POST.get(f'series_{ejercicio_id}') or None

            RutinaEjercicio.objects.create(
                rutina=rutina,
                ejercicio_id=ejercicio_id,
                peso=peso,
                repeticiones=reps,
                series=series
            )

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

@login_required #type: ignore
def actualizar_ejercicio(request):
    if request.method == "POST":
        data = json.loads(request.body)

        r = RutinaEjercicio.objects.get(id=data['id'])

        valor = data['value']

        # convertir según campo
        if valor == "":
            valor = None
        else:
            if data['field'] == 'peso':
                valor = float(valor)
            else:
                valor = int(valor)

        setattr(r, data['field'], valor)
        r.save()

        return JsonResponse({'status': 'ok'})