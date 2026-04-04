from django.urls import path
from . import views

app_name = 'rutinas'

urlpatterns = [
    path('mis_rutinas/', views.rutinas, name='rutinas'),
    path('crear-rutina/', views.crear_rutina, name='crear-rutina'),
    path('centro_rutinas/', views.centro_rutinas, name='centro-rutinas'),
    path('cargar_ejercicio/', views.cargar_ejercicio, name='cargar-ejercicio'),
    path('actualizar-ejercicio/', views.actualizar_ejercicio, name='actualizar_ejercicio'),#type: ignore
    path('profesor/', views.rutinas_profesor, name='ver-rutinas'),
    path('editar/<int:rutina_id>/', views.editar_rutina, name='editar-rutina'),
    path('eliminar/<int:rutina_id>/', views.eliminar_rutina, name='eliminar-rutina'),
    path('eliminar-ejercicio/<int:ejercicio_id>/', views.eliminar_ejercicio, name='eliminar-ejercicio'),
]