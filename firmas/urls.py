from django.urls import path
from . import views

urlpatterns = [

    path("panel/", views.panel_qr, name="panel_qr"), # este es el panel de QR
    path("api/regenerar_qr/", views.api_regenerar_qr, name="api_regenerar_qr"),
    path("marcar/", views.marcar_asistencia, name="marcar_asistencia"), #marcar es para la asistencia del docente
    path("directora/asistencias/", views.asistencias_admin, name="asistencias_admin"),
]
