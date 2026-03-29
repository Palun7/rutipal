from django.shortcuts import redirect, render
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

@login_required
def rutinas_profesor(request):
    if request.user != Usuario.objects.filter(tipo_usuario='profesor').first():
        return redirect('rutinas:rutinas')

    usuarios = Usuario.objects.all().prefetch_related(
        'diarutina_set__ejercicios__ejercicio'
    )

    return render(request, 'rutinas/ver-rutinas.html', {
        'usuarios': usuarios
    })

@login_required
def editar_rutina(request, rutina_id):
    rutina = get_object_or_404(DiaRutina, id=rutina_id)

    if request.user != Usuario.objects.filter(tipo_usuario='profesor').first():
        return redirect('rutinas:rutinas')

    if request.method == "POST" and 'agregar' in request.POST:
        ejercicio_id = request.POST.get('ejercicio_id')
        reps = request.POST.get('reps') or None
        series = request.POST.get('series') or None
        peso = request.POST.get('peso') or None

        obj, creado = RutinaEjercicio.objects.get_or_create(
            rutina=rutina,
            ejercicio_id=ejercicio_id,
            defaults={
                'repeticiones': reps,
                'series': series,
                'peso': peso
            }
        )

        if not creado:
            obj.repeticiones = reps
            obj.series = series
            obj.peso = peso
            obj.save()

    ejercicios = rutina.ejercicios.all()# type: ignore
    todos_ejercicios = Ejercicio.objects.all()

    return render(request, 'rutinas/editar-rutina.html', {
        'rutina': rutina,
        'ejercicios': ejercicios,
        'todos_ejercicios': todos_ejercicios
    })

@login_required
def eliminar_rutina(request, rutina_id):
    rutina = get_object_or_404(DiaRutina, id=rutina_id)

    if request.user != Usuario.objects.filter(tipo_usuario='profesor').first():

        return redirect('rutinas:rutinas')

    if request.method == "POST":
        rutina.delete()

    return redirect('rutinas:ver-rutinas')

@login_required
def eliminar_ejercicio(request, ejercicio_id):
    if request.user != Usuario.objects.filter(tipo_usuario='profesor').first():

        return JsonResponse({'error': 'No autorizado'}, status=403)

    if request.method == "POST":
        r = get_object_or_404(RutinaEjercicio, id=ejercicio_id)
        r.delete()
        return JsonResponse({'status': 'ok'})

    return JsonResponse({'error': 'Método no permitido'}, status=405)