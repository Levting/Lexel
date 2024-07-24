from django.urls import path
from . import views

urlpatterns = [
    # Vista principal
    path('',
         views.index, name='calidad_producto_index'),

    # --- ARMONICOS ---

    # Vista de Armónicos
    path('armonicos',
         views.vista_armonicos, name='vista_armonicos'),

    # Vista para crear un/unos archivos de armonicos
    path('armonicos/crear/',
         views.vista_crear_armonico, name='vista_crear_armonico'),

    # Crear un archivo de armonicos
    path('armonicos/crear/unico',
         views.crear_armonico_unico, name='crear_armonico_unico'),

    # Crear varios archivos de armonicos
    path('armonicos/crear/lote',
         views.crear_armonico_lote, name='crear_armonico_lote'),

    # Obtener los detalles de un archivo de armonicos
    path('armonicos/<int:archivo_id>',
         views.vista_armonico_detalle, name='armonico_detalle'),

    # Eliminar un archivo de armonicos
    path('armonicos/eliminar/<int:archivo_id>',
         views.eliminar_armonico, name='eliminar_armonico'),

     # --- TENDENCIAS ---

    # Vista de Tendencias
    path('tendencias',
         views.vista_tendencias, name='vista_tendencias'),

     # Vista para crear un/unos archivos de tendencias
    path('tendencias/crear',
         views.vista_crear_tendencia, name='vista_crear_tendencia'),

     # Crear un archivo de tendencias
     path('tendencias/crear/unico',
           views.crear_tendencia_unico, name='crear_tendencia_unico'),

     # Crear varios arrchivos de tendencias
     path('tendencias/crear/lote',
           views.crear_tendencia_lote, name='crear_tendencia_lote'),
          
     # Obtener los detalles de un archivo de tendencias
     path('tendencias/<int:archivo_id>',
           views.vista_tendencia_detalle, name='tendencia_detalle'),

     # Eliminar un archivo de tendencias
     path('tendencias/eliminar/<int:archivo_id>',
           views.eliminar_tendencia, name='eliminar_tendencia'),
]
