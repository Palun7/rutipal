from django.db import models

class Ejercicio(models.Model):
    nombre = models.CharField(max_length=100)
    musculo = models.CharField(max_length=100)
    descripcion = models.TextField()
    imagen = models.ImageField(upload_to='ejercicios/', blank=True, null=True)
    url = models.URLField(blank=True, null=True)

    class Meta:
        unique_together = ('nombre', 'musculo')
        verbose_name = "Ejercicio"
        verbose_name_plural = "Ejercicios"

    def __str__(self):
        return f"{self.nombre} ({self.musculo})"

class DiaRutina(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    mes = models.CharField(max_length=20)
    dia = models.IntegerField()

    class Meta:
        unique_together = ('usuario', 'mes', 'dia')
        verbose_name = "Día de Rutina"
        verbose_name_plural = "Días de Rutina"
        ordering = ['mes', 'dia']

    def __str__(self):
        return f"{self.usuario.username} - {self.mes} {self.dia}"

class RutinaEjercicio(models.Model):
    rutina = models.ForeignKey(DiaRutina, on_delete=models.CASCADE, related_name='ejercicios')
    ejercicio = models.ForeignKey(Ejercicio, on_delete=models.CASCADE)

    peso = models.FloatField(null=True, blank=True)
    repeticiones = models.IntegerField(null=True, blank=True)
    series = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = "Ejercicio en Rutina"
        verbose_name_plural = "Ejercicios en Rutina"

    def __str__(self):
        return f"{self.rutina.usuario.username} - {self.rutina.mes}/{self.rutina.dia} - {self.ejercicio.nombre}"