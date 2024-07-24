from django.db import models


def cargar_a(instancia, nombre_archivo):
    """
    Devuelve la ruta de carga del archivo basado en su categoría
    """
    if instancia.categoria == 'armonico':
        return f'archivos/armonicos/{nombre_archivo}'
    elif instancia.categoria == 'tendencia':
        return f'archivos/tendencias/{nombre_archivo}'
    else:
        return f'archivos/{nombre_archivo}'


class Archivo(models.Model):
    """
    Modelo para almacenar los archivos subidos por el usuario
    """

    # Definir las opciones de categoría
    CATEGORIA = [
        ('armonico', 'Armonico'),
        ('tendencia', 'Tendencia'),
        ('otro', 'Otro'),
    ]

    archivo = models.FileField(upload_to=cargar_a)
    categoria = models.CharField(
        max_length=20, choices=CATEGORIA, default='otro')
    subido_el = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.archivo.name


class ArchivoInfo(models.Model):
    """
    Modelo para almacenar la información extraída de los archivos subidos en un campo JSON
    """
    # Definir la relacion inversa con el modelo, para acceder al ubjeto Archivo desde ArchivoInfo
    archivo = models.ForeignKey(Archivo,
                                on_delete=models.CASCADE,
                                related_name='info')
    data = models.JSONField(default=dict)

    def __str__(self):
        return f'{self.archivo.archivo.name} - {self.data}'
