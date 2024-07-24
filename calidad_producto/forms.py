from django import forms
from .models import Archivo


class ArchivoForm(forms.ModelForm):
    """
    Formulario para subir un archivo, extendido de un modelo de archivo.
    """
    class Meta:
        model = Archivo
        fields = ['archivo']


class ArchivoLoteForm(forms.Form):
    """
    Formulario para subir más de un archivo xls.
    """
    #archivos = forms.FileField(
    #    widget=forms.ClearableFileInput(attrs={'multiple': True}),
    #    required=True,
    #    label='Selecciona archivos'
    #)
