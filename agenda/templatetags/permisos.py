from django import template
from agenda.permisos import es_directora  # tu función original

register = template.Library()

# nombre del filtro que vas a usar en el template
@register.filter(name='es_directora')
def es_directora_filter(user):
    return es_directora(user)
