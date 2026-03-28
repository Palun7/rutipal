from django.db import models

class Ejercicio(models.Model):
    nombre = models.CharField(max_length=100)
    musculo = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='ejercicios/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"{self.nombre} ({self.musculo})"

class DiaRutina(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    mes = models.CharField(max_length=20)
    dia = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.usuario.username} - {self.mes} {self.dia}"

class RutinaEjercicio(models.Model):
    rutina = models.ForeignKey(DiaRutina, on_delete=models.CASCADE)
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)

    peso = models.FloatField(null=True, blank=True)
    repeticiones = models.IntegerField(null=True, blank=True)
    series = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.ejercicio.nombre} ({self.ejercicio.musculo}): {self.repeticiones} reps x {self.series} series, {self.peso} kg"