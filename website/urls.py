from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),

    path(
    'guardar-consulta/',
    views.guardar_consulta,
    name='guardar_consulta'
),
]