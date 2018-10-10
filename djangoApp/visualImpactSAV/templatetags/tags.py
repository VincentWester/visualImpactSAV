from django.template.defaulttags import register
import constants


@register.filter
def nb_libelle(value, libelle):
    return value[libelle]

@register.filter
def have_libelle_from_code(value):
    for status in constants.SAV_FILE_STATUS_CHOICES:
        if value == status[0]:
            return status[1]

    return ""

@register.filter
def have_css_class_from_code(value):
    if value == 'O':
        return 'opened'
    
    if value == 'C':
        return 'closed'

    if value == 'IP':
        return 'in-progress'

    if value == 'P':
        return 'problem'

    return ''
