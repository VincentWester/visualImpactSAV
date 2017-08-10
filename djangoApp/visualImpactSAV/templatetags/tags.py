from django import template
from django.template.defaulttags import register


@register.filter
def count_by_libelle(values, libelle):  
    return len(values.filter(sav_file_status__libelle = libelle)) 