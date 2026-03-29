from django.db import models
from django.contrib.auth.models import AbstractUser

class Usuario(AbstractUser):
    dni = models.CharField(max_length=8, unique=True, blank=True, null=True)
    foto = models.ImageField(upload_to='fotos_usuarios/', blank=True, null=True)
    telefono = models.CharField(max_length=10, blank=True, null=True)
    tipo_usuario = models.CharField(max_length=20, choices=[
        ('alumno', 'Alumno'),
        ('profesor', 'Profesor'),
    ], default='alumno')

    @property
    def is_profesor(self):
        return self.tipo_usuario == 'profesor'

    @property
    def is_alumno(self):
        return self.tipo_usuario == 'alumno'

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"

    def __str__(self):
        return self.username