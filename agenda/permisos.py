from django.contrib.auth.models import User

def es_directora(user):
    return user.groups.filter(name='Directora').exists()