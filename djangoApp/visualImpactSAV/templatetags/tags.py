from django.template.defaulttags import register
import constants


@register.filter
def nb_libelle(value, libelle):
    return value[libelle]


@register.filter
def have_libelle_from_code(value, type_list):
    tuple_list = ()
    if type_list == 'status':
        tuple_list = constants.SAV_FILE_STATUS_CHOICES
        print 'ici'
    elif type_list == 'waranty':
        tuple_list = constants.SAV_FILE_WARANTY_TYPE_CHOICES
        print 'la'
    
    print tuple_list
    print value

    for status in tuple_list:
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
