from django.db import models
from django.contrib.auth.models import User

class PerfilDocente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    anio = models.IntegerField(
        choices=[(i, f"{i}° Año") for i in range(1, 7)],
        null=False, blank=False

    )

    def __str__(self):
        return f"{self.user.username} - {self.anio}° año"
