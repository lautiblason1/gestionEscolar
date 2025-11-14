from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from datetime import date

class FirmaDiaria(models.Model):
    docente = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_staff': False})
    fecha = models.DateField(default=date.today)
    presente = models.BooleanField(default=True)   # True si firmó
    observacion = models.TextField(blank=True, null=True)  # Ej: "Llegó tarde"

    def __str__(self):
        return f"{self.docente.username} - {self.fecha} ({'Presente' if self.presente else 'Ausente'})"
