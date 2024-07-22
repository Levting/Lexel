from django import forms
from .models import Archivo


class ArchivoForm(forms.ModelForm):
    """
    Formulario para subir un archivo, extendido de un modelo de archivo.
    """
    class Meta:
        model = Archivo
        fields = ['archivo']

    def control_nombre_archivo(self):
        archivo = self.cleaned_data['archivo']
        print(archivo.name)
        if Archivo.objects.filter(archivo=archivo).exists():
            raise forms.ValidationError(
                'El archivo ya existe en la base de datos.')
        return archivo
