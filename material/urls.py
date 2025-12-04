from django.urls import path
from . import views

urlpatterns = [
    # Dashboard docente
    path("dashboard/", views.dashboard_docente, name="dashboard_docente"),

    # Directora (subida y gestión de materiales)
    path("directora/materiales/", views.lista_materiales_admin, name="lista_materiales_admin"),
    path("directora/materiales/subir/", views.subir_material, name="subir_material"),

    # Descarga segura
    path("material/<int:material_id>/descargar/", views.descargar_material, name="descargar_material"),
]

