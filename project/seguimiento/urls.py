from django.urls import path
from . import views

app_name = 'seguimiento'

urlpatterns = [
    path('cargar-registro/', views.cargar_registro, name='cargar-registro'),
    path('ver-registros/', views.ver_registros, name='ver-registros'),
]