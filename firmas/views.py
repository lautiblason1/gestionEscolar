from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.decorators import login_required, user_passes_test 
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.db.models.functions import TruncDate

from .models import QRActivo, TokenAsistencia, Asistencia
from .utils import generar_token, generar_qr_imagen

# Importá la función es_directora donde la tengas (ideal: agenda/permisos.py)
from agenda.permisos import es_directora


@login_required
@user_passes_test(es_directora)
def panel_qr(request):
    """
    Página para la directora: muestra el QR actual (si existe) y el panel.
    El template contiene JS que llama a api_regenerar_qr cada 60s.
    """
    qr = QRActivo.objects.filter(activo=True).order_by('-actualizado').first()
    qr_url = None
    if qr:
        qr_url = f"{qr.token}"  # el template construye la ruta de imagen, o podés pasar full path
        # mejor pasar la URL de media: (si querés)
        # qr_image = f"{settings.MEDIA_URL}qr_{qr.token}.png"
    return render(request, "firmas/panel_qr.html", {"qr": qr, "qr_url": qr_url})


@login_required
@user_passes_test(es_directora)
def api_regenerar_qr(request):
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    # Desactivar QR previo (pero no lo borremos)
    QRActivo.objects.filter(activo=True).update(activo=False)

    token = generar_token()
    expira = timezone.now() + timedelta(minutes=1)

    qr_obj = QRActivo.objects.create(
        token=token,
        expira=expira,
        activo=True
    )

    qr_url_full = f"http://{request.get_host()}/firmas/marcar/?token={token}"
    qr_image_url = generar_qr_imagen(qr_url_full, token)

    return JsonResponse({
        "token": token,
        "expira": expira.strftime("%Y-%m-%d %H:%M:%S"),
        "qr_image": qr_image_url
    })

@login_required
def marcar_asistencia(request):
    token = request.GET.get("token")
    if not token:
        return redirect("dashboard_docente")

    # Validar QR activo
    try:
        qr = QRActivo.objects.get(token=token, activo=True)
    except QRActivo.DoesNotExist:
        return redirect("dashboard_docente")

    if timezone.now() > qr.expira:
        return redirect("dashboard_docente")

    # Evitar duplicados por día
    fecha_hoy = timezone.now().date()
    if Asistencia.objects.filter(docente=request.user, fecha=fecha_hoy).exists():
        return redirect("dashboard_docente")

    # Registrar asistencia
    Asistencia.objects.create(
        docente=request.user,
        fecha=timezone.now(),
        token_usado=token
    )

    # Inactivar el QR
    qr.activo = False
    qr.save()

    # Redirigir al dashboard del docente
    return redirect("dashboard_docente")

@login_required
@user_passes_test(es_directora)
def asistencias_admin(request):
    asistencias = Asistencia.objects.all().order_by('-fecha')
    return render(request, 'firmas/asistencias_admin.html', {"asistencias": asistencias})

