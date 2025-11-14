from django.db import models
from django.contrib.auth.models import User  # Usamos el User de Django

class Evento(models.Model):
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True, null=True)
    fecha = models.DateField()
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    # Si querés relacionarlo con material
    # materiales = models.ManyToManyField('material.Material', blank=True)

    def __str__(self):
        return f"{self.titulo} ({self.fecha})"

