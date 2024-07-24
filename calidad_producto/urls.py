from django.urls import path
from . import views

urlpatterns = [
    # /calidad_producto
    path('',
         views.index, name='calidad_producto_index'),

    # /calidad_producto/armonicos
    path('armonicos',
         views.vista_armonicos, name='vista_armonicos'),

     path('armonicos/crear/',
          views.vista_crear_armonico, name='vista_crear_armonico'),

    # /calidad_producto/armonicos/crear/unico?lote
    path('armonicos/crear/unico',
         views.crear_armonico_unico, name='crear_armonico_unico'),

    path('armonicos/crear/lote',
         views.crear_armonico_lote, name='crear_armonico_lote'),

    # /calidad_producto/armonicos/#
    path('armonicos/<int:archivo_id>',
         views.vista_armonico_detalle, name='armonico_detalle'),

    # /calidad_producto/armonicos/eliminar/#
    path('armonicos/eliminar/<int:archivo_id>',
         views.eliminar_armonico, name='eliminar_armonico'),
]
