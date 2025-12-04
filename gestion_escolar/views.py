from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from agenda.permisos import es_directora

def login_view(request):
    # ⭐ Primero obtener next (GET o POST)
    next_url = request.GET.get("next") or request.POST.get("next")

    # ⭐ Si el usuario ya está logueado → respetar next si existe
    if request.user.is_authenticated:
        if next_url not in [None, "", "None"]:
            return redirect(next_url)

        if es_directora(request.user):
            return redirect("agenda_index")
        return redirect("home")

    # ⭐ Si NO está autenticado → procesamos el login
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)

            # Después del login: respetar next si existe
            if next_url not in [None, "", "None"]:
                return redirect(next_url)

            # Sin next → redirigir por rol
            if es_directora(user):
                return redirect("agenda_index")
            return redirect("home")

        messages.error(request, "Credenciales incorrectas")

    return render(request, "login.html", {"next": next_url})



def logout_view(request):
    logout(request)
    return redirect("login")  # te lleva al login luego de cerrar sesión
