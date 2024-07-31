from django.db import models


def cargar_a(instancia, nombre_archivo):
    if instancia.categoria.nombre == "Armónico":
        return f'archivos/armonicos/{nombre_archivo}'
    elif instancia.categoria.nombre == "Tendencia":
        return f'archivos/tendencias/{nombre_archivo}'
    else:
        return f'archivos/{nombre_archivo}'


class Categoria(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Tipo(models.Model):
    nombre = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre


class Analizador(models.Model):
    nombre = models.CharField(max_length=50)
    voltaje_a = models.CharField(max_length=50)
    voltaje_b = models.CharField(max_length=50)
    voltaje_c = models.CharField(max_length=50, blank=True, null=True)
    flicker_a = models.CharField(max_length=50)
    flicker_b = models.CharField(max_length=50)
    flicker_c = models.CharField(max_length=50, blank=True, null=True)
    vthd_a = models.CharField(max_length=50)
    vthd_b = models.CharField(max_length=50)
    vthd_c = models.CharField(max_length=50, blank=True, null=True)
    desbalance = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.nombre


class Archivo(models.Model):
    archivo = models.FileField(upload_to=cargar_a)
    subido_el = models.DateTimeField(auto_now_add=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    analizador = models.ForeignKey(Analizador, on_delete=models.CASCADE)
    informacion = models.JSONField(default=dict)

    def __str__(self):
        return self.archivo.name
