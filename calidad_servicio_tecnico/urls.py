from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='calidad_servicio_tecnico_index'),  # /calidad_servicio_tecnico
]
