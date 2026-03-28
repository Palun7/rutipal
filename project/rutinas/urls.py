from django.urls import path
from . import views

app_name = 'rutinas'

urlpatterns = [
    path('mis_rutinas/', views.rutinas, name='rutinas'),
    path('crear/', views.crear_rutina, name='crear-rutina'),
    path('centro_rutinas/', views.centro_rutinas, name='centro-rutinas'),
    path('cargar_ejercicio/', views.cargar_ejercicio, name='cargar-ejercicio'),
]