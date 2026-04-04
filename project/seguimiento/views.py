from django.shortcuts import render, redirect
from .models import Registro, Medida
from django.contrib.auth.decorators import login_required

@login_required
def cargar_registro(request):
    usuario = request.user

    if request.method == 'POST':

        peso = request.POST.get('peso') or None
        comentario = request.POST.get('comentario')
        foto = request.FILES.get('foto')

        registro = Registro.objects.create(
            usuario=usuario,
            peso=float(peso) if peso else None,
            comentario=comentario,
            foto=foto
        )

        nombres = request.POST.getlist('medida_nombre[]')
        valores = request.POST.getlist('medida_valor[]')
        unidades = request.POST.getlist('medida_unidad[]')

        for nombre, valor, unidad in zip(nombres, valores, unidades):
            if nombre and valor:

                if Medida.objects.filter(registro=registro, nombre=nombre).exists():
                    continue

                Medida.objects.create(
                    registro=registro,
                    nombre=nombre.capitalize().strip(),
                    valor=float(valor),
                    unidad=unidad
                )

        return redirect('usuarios:perfil')

    return render(request, 'seguimiento/cargar-registro.html')

@login_required
def ver_registros(request):
    registros = Registro.objects.filter(usuario=request.user)
    return render(request, 'seguimiento/ver-registros.html', {'registros':registros})