from django.urls import path
from . import views

urlpatterns = [
    # /calidad_producto
    path('', views.index, name='calidad_producto_index'),

    # /calidad_producto/armonicos
    path('armonicos/', views.vista_armonicos, name='vista_armonicos'),

    # /calidad_producto/armonicos/crear
    path('armonicos/crear', views.crear_armonico, name='crear_armonico'),

    # /calidad_producto/armonicos/#
    path('armonicos/<int:archivo_id>', views.vista_armonico_detalle,
         name='armonico_detalle'),

    # /calidad_producto/armonicos/eliminar/#
    path('armonicos/eliminar/<int:archivo_id>',
         views.eliminar_armonico, name='eliminar_armonico'),
]
