from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect
from firmas.models import Asistencia
from .models import Material  # Ajustar según tu modelo
from agenda.permisos import es_directora
from .forms import MaterialForm

@login_required
def dashboard_docente(request):
    usuario = request.user

    # Traer el perfil del docente
    perfil = usuario.perfildocente  

    # Traer asistencias del docente
    asistencias = Asistencia.objects.filter(docente=usuario).order_by("-fecha")

    # Filtrar materiales según el año del docente
    materiales = Material.objects.filter(anio=perfil.anio).order_by("-id")

    context = {
        "usuario": usuario,
        "perfil": perfil,
        "asistencias": asistencias,
        "materiales": materiales,
    }

    return render(request, "material/dashboard_docente.html", context)

from django.contrib import messages




@login_required
@user_passes_test(es_directora)
def subir_material(request):
    if request.method == "POST":
        form = MaterialForm(request.POST, request.FILES)
        if form.is_valid():
            material = form.save(commit=False)
            material.subido_por = request.user
            material.save()
            messages.success(request, "Material subido correctamente.")
            return redirect("lista_materiales_admin")
    else:
        form = MaterialForm()

    return render(request, "material/subir_material.html", {"form": form})


@login_required
@user_passes_test(es_directora)
def lista_materiales_admin(request):
    materiales = Material.objects.order_by("-fecha_subida")
    return render(request, "material/lista_materiales_admin.html", {
        "materiales": materiales
    })

from django.http import HttpResponse

@login_required
def descargar_material(request, material_id):
    material = Material.objects.get(id=material_id)

    # Si NO es directora → validar año
    if not es_directora(request.user):
        perfil = request.user.perfildocente
        if material.anio != perfil.anio:
            return HttpResponse("No tienes permiso para descargar este material.", status=403)

    return redirect(material.archivo.url)

