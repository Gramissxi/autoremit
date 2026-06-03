from django.urls import path
from . import views
from .views import remito_create, remito_detalle, remitos_por_empresa

urlpatterns = [
    path('', views.index, name='index'),
    path('remitos/nuevo/', remito_create, name='remito_create'),
    path('remitos/<int:remito_id>/cargar-dias/', views.remito_cargar_dias, name='remito_cargar_dias'),
    path('remitos/<int:pk>/', views.remito_detalle, name='remitoDetalle'),
    path('empresa/<int:empresa_id>/remitos/', views.remitos_por_empresa, name='remitos_por_empresa'),
    #path('remitos/<int:pk>/descargar/', views.descargar_remito_pdf, name='descargar_remito_pdf'),


]
