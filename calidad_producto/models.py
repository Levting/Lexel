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
    Modelo para almacenar la información extraída de los archivos subidos
    """
    archivo = models.ForeignKey(
        Archivo, on_delete=models.CASCADE, related_name='info')
    nombre_columna = models.CharField(max_length=100)
    valor = models.FloatField()

    # data = models.JSONField()

    def __str__(self):
        return self.nombre_columna + ' - ' + str(self.valor)
