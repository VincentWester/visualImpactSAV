from django import template
from django.template.defaulttags import register

@register.filter
def nb_libelle(value, libelle):
    return value[libelle]