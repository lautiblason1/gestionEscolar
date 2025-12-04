from django.db import models
from django.contrib.auth.models import User

class Material(models.Model):
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, null=True)
    archivo = models.FileField(upload_to='materiales/')
    fecha_subida = models.DateTimeField(auto_now_add=True)
    subido_por = models.ForeignKey(User, on_delete=models.CASCADE)

    anio = models.IntegerField(
        choices=[(i, f"{i}° Año") for i in range(1, 7)],
        null=False,
        blank=False
    )

    def __str__(self):
        return self.titulo
