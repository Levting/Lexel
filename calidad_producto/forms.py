from django import forms
from .models import Archivo


class ArchivoForm(forms.ModelForm):
    """
    Formulario para subir un archivo, extendido de un modelo de archivo.
    """
    class Meta:
        model = Archivo
        fields = ['archivo']
