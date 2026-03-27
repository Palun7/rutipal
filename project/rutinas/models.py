from django.db import models

class Ejercicio(models.Model):
    nombre = models.CharField(max_length=100)
    musculo = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='ejercicios/', blank=True, null=True)
    video_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.nombre

class EjercicioAplicado(models.Model):
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)
    repeticiones = models.IntegerField()
    series = models.IntegerField()
    kg = models.FloatField()

    def __str__(self):
        return f"{self.ejercicio.nombre} - {self.repeticiones} reps / {self.series} series / {self.kg} kg"

class DiaRutina(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    mes = models.CharField(max_length=20)
    dia = models.CharField(max_length=20)
    ejercicio = models.ManyToManyField(EjercicioAplicado)

    def __str__(self):
        return f"{self.usuario.username} - {self.mes} {self.dia}"