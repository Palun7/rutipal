from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def rutinas(request):
    user = request.user
    return render(request, 'rutinas/rutinas.html', {'usuario': user})