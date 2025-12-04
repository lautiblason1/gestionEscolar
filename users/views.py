from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .forms import RegistroDocenteForm

def registro_docente(request):
    if request.method == 'POST':
        form = RegistroDocenteForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            # agregar al grupo "docentes"
            grupo = Group.objects.get(name='docentes')
            user.groups.add(grupo)

            return redirect('login')

    else:
        form = RegistroDocenteForm()

    return render(request, 'users/registro.html', {'form': form})
