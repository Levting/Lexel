from django.contrib import admin
from .models import Archivo, ArchivoInfo


class ArchivoAdmin(admin.ModelAdmin):
    readonly_fields = ('subido_el',)


# Register your models here.
admin.site.register(Archivo, ArchivoAdmin)
admin.site.register(ArchivoInfo)
# admin.site.register(ArchivoAdmin)
