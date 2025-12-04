from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TokenAsistencia(models.Model):
    # opcional, lo podés usar más adelante; si no lo necesitás podés borrarlo
    token = models.CharField(max_length=50, unique=True)
    creado = models.DateTimeField(default=timezone.now)
    expirado = models.BooleanField(default=False)

    def __str__(self):
        return self.token

class Asistencia(models.Model):
    docente = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha = models.DateTimeField(default=timezone.now)   # guardamos fecha+hora
    token_usado = models.CharField(max_length=50)

    def __str__(self):
        return f"Asistencia {self.docente.username} - {self.fecha}"

class QRActivo(models.Model):
    token = models.CharField(max_length=50, unique=True)
    expira = models.DateTimeField()            # <- necesario
    actualizado = models.DateTimeField(auto_now=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"QR Activo ({'Activo' if self.activo else 'Inactivo'})"
