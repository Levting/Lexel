from django.contrib import admin
from .models import Archivo, Categoria, Tipo, Analizador


class ArchivoAdmin(admin.ModelAdmin):
    readonly_fields = ('subido_el',)


# Register your models here.
admin.site.register(Archivo, ArchivoAdmin)
admin.site.register(Categoria)
admin.site.register(Tipo)
admin.site.register(Analizador)
# admin.site.register(ArchivoAdmin)
