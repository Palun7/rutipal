from django.db import models

class Registro(models.Model):
    usuario = models.ForeignKey('usuarios.Usuario', on_delete=models.CASCADE)
    fecha = models.DateField(auto_now_add=True)

    peso = models.FloatField(blank=True, null=True)

    foto = models.ImageField(upload_to='registro/%Y/%m/', blank=True, null=True)
    comentario = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Registro"
        verbose_name_plural = "Registros"
        ordering = ['-fecha']

    def __str__(self):
        return f'{self.usuario.username} - {self.fecha}'


class Medida(models.Model):
    UNIDADES = [
        ('m', 'Metros'),
        ('cm', 'Centímetros'),
        ('kg', 'Kilogramos'),
        ('mm', 'Milímetros'),
    ]

    registro = models.ForeignKey(Registro, on_delete=models.CASCADE, related_name='medidas_registro')
    nombre = models.CharField(max_length=50)
    valor = models.FloatField()
    unidad = models.CharField(max_length=5, choices=UNIDADES, default='cm')

    class Meta:
        verbose_name = 'Medida'
        verbose_name_plural = 'Medidas'
        unique_together = ('registro', 'nombre')

    def __str__(self):
        return f'{self.nombre} - {self.valor}{self.unidad}'