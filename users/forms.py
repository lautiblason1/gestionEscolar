from django import forms
from django.contrib.auth.models import User
import re

class RegistroDocenteForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    anio = forms.ChoiceField(
        choices=[(i, f"{i}° Año") for i in range(1, 7)],
        required=True,
        label="Año"
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']

    # -------------------------
    # VALIDACIÓN PERSONALIZADA
    # -------------------------

    def clean_first_name(self):
        nombre = self.cleaned_data['first_name']

        # Solo letras y espacios
        if not re.match(r'^[A-Za-zÁÉÍÓÚÑáéíóúñ ]+$', nombre):
            raise forms.ValidationError("El nombre solo puede contener letras.")

        # Máximo 15 caracteres
        if len(nombre) > 15:
            raise forms.ValidationError("El nombre no puede superar los 15 caracteres.")

        return nombre

    def clean_last_name(self):
        apellido = self.cleaned_data['last_name']

        if not re.match(r'^[A-Za-zÁÉÍÓÚÑáéíóúñ ]+$', apellido):
            raise forms.ValidationError("El apellido solo puede contener letras.")

        if len(apellido) > 15:
            raise forms.ValidationError("El apellido no puede superar los 15 caracteres.")

        return apellido
