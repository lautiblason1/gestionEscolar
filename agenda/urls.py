from django.urls import path
from . import views

urlpatterns = [
    path('', views.lista_eventos, name='agenda_index'),
    path('<int:id>/', views.detalle_evento, name='detalle_evento'),
    path('crear/', views.crear_evento, name='crear_evento'),
    path('<int:id>/editar/', views.editar_evento, name='editar_evento'),
    path('<int:id>/eliminar/', views.eliminar_evento, name='eliminar_evento'),
]
