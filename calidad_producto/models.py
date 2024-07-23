from django.db import models

# Create your models here.


class Archivo(models.Model):
    """
    Modelo para almacenar los archivos subidos por el usuario
    """
    archivo = models.FileField(upload_to='archivos/')
    subido_el = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.archivo.name


class ArchivoInfo(models.Model):
    """
    Modelo para almacenar la información extraída de los archivos subidos en un campo JSON
    """
    # archivo = models.ForeignKey(Archivo, on_delete=models.CASCADE, related_name='info')
    # nombre_columna = models.CharField(max_length=100)
    # valor = models.FloatField()

    # Definir la relacion inversa con el modelo, para acceder al ubjeto Archivo desde ArchivoInfo
    archivo = models.ForeignKey(
        Archivo, on_delete=models.CASCADE, related_name='info')
    data = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.archivo.archivo.name} - {self.data}'
