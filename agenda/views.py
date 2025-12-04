from django.shortcuts import render, get_object_or_404, redirect
from .models import Evento
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .permisos import es_directora



"""Lista eventos mejorada"""

import calendar
from datetime import date
from django.shortcuts import render
from .models import Evento

@login_required
def lista_eventos(request):
    from django.shortcuts import render
from datetime import date, datetime, timedelta
import calendar
from .models import Evento
from datetime import date


MESES_ES = [
    "", "Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio",
    "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"
]


def lista_eventos(request):
    
    # 1. Obtener mes/año actual por parámetros GET
    hoy = date.today()
    mes = int(request.GET.get("mes", hoy.month))
    año = int(request.GET.get("año", hoy.year))

    # 2. Construir calendario
    cal = calendar.Calendar(firstweekday=0)  # lunes=0
    semanas = cal.monthdatescalendar(año, mes)

    # 3. Traer eventos del mes
    eventos = Evento.objects.filter(fecha__year=año, fecha__month=mes)

    # 4. Transformar estructura para el template
    calendario = []
    for semana in semanas:
        fila = []
        for dia in semana:
            fila.append({
                "dia": dia.day,
                "fecha": dia,
                "pertenece": (dia.month == mes),
                "eventos": [e for e in eventos if e.fecha == dia]
            })
        calendario.append(fila)

    # 5. Datos para navegación
    mes_nombre = MESES_ES[mes]

    # mes anterior
    if mes == 1:
        mes_anterior, año_anterior = 12, año - 1
    else:
        mes_anterior, año_anterior = mes - 1, año

    # mes siguiente
    if mes == 12:
        mes_siguiente, año_siguiente = 1, año + 1
    else:
        mes_siguiente, año_siguiente = mes + 1, año

    # 6. Crear el context (aquí lo agregamos)
    context = {
        "calendario": calendario,
        "mes_nombre": mes_nombre,
        "mes": mes,
        "año": año,
        "mes_anterior": mes_anterior,
        "año_anterior": año_anterior,
        "mes_siguiente": mes_siguiente,
        "año_siguiente": año_siguiente,
        "today": hoy,
        "es_directora": es_directora(request.user),
    }

    # 7. Renderizar
    return render(request, "agenda/lista_eventos.html", context)




@login_required
def detalle_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    return render(request, 'agenda/detalle_evento.html', {'evento': evento})

"""Crear evento"""
@login_required
def crear_evento(request):
    if not es_directora(request.user):
        return HttpResponseForbidden("No tenés permiso para crear eventos.")
    
    # Obtener fecha de la query string (si viene del calendario)
    fecha_preseleccionada = request.GET.get('fecha', '')

    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')

        Evento.objects.create(
            titulo=titulo,
            descripcion=descripcion,
            fecha=fecha,
            hora=hora,
            creado_por=request.user
        )
        return redirect('agenda_index')

    return render(request, 'agenda/crear_evento.html', {
        'fecha_preseleccionada': fecha_preseleccionada
    })


@login_required
def editar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if evento.creado_por != request.user:
        return HttpResponseForbidden("No tenés permiso para editar este evento.")
    
    if request.method == 'POST':
        evento.titulo = request.POST.get('titulo')
        evento.descripcion = request.POST.get('descripcion')
        evento.fecha = request.POST.get('fecha')
        evento.hora = request.POST.get('hora')
        evento.save()
        return redirect('detalle_evento', id=evento.id)
    return render(request, 'agenda/editar_evento.html', {'evento': evento})

@login_required
def eliminar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if evento.creado_por != request.user:
        return HttpResponseForbidden("No tenés permiso para eliminar este evento.")
    evento.delete()
    return redirect('agenda_index')

