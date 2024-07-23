from django.urls import path
from .views import inicio, vista_armonicos, crear_armonico, vista_armonico_detalle, eliminar_armonico

urlpatterns = [
    path('', inicio, name='inicio'),  # /calidad_producto
    path('armonicos/', vista_armonicos, name='armonicos'),  # /calidad_producto/armonicos
    path('armonicos/crear', crear_armonico, name='crear_armonico'),  # /calidad_producto/armonicos/crear
    path('armonicos/<int:archivo_id>', vista_armonico_detalle, name='armonico_detalle'), # /calidad_producto/armonicos/1
    path('armonicos/eliminar/<int:archivo_id>', eliminar_armonico, name='eliminar_armonico'), 
]
