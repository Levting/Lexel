from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='principal_index'),
]
