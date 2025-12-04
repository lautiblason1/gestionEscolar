from django.shortcuts import redirect
from django.urls import reverse

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        path = request.path

        # Rutas permitidas sin autenticación
        open_paths = [
            '/login/',
            '/registro/',
            '/logout/',
            '/admin/',
            '/',
        ]

        # ---- EXCEPCIONES IMPORTANTES ----

        # Archivos estáticos
        if path.startswith('/static/'):
            return self.get_response(request)

        # Archivos media
        if path.startswith('/media/'):
            return self.get_response(request)

        # Favicon
        if path == '/favicon.ico':
            return self.get_response(request)

        # Rutas abiertas definidas manualmente
        if any(path.startswith(p) for p in open_paths):
            return self.get_response(request)

        # ---- CONTROL DE LOGIN ----
        if not request.user.is_authenticated:
            login_url = reverse('login')
            next_url = request.get_full_path()
            return redirect(f"{login_url}?next={next_url}")

        # Si está autenticado, continuar normalmente
        return self.get_response(request)


