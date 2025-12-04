from django.shortcuts import render

def home(request):
    # Renderizamos un template en lugar de HttpResponse
    return render(request, "core/home.html")
