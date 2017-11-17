from django.forms import ModelForm, CharField, ValidationError
from .models import SAV_file, Event, Designation
from django.utils.translation import ugettext_lazy as _
#Essai avec exclude

class SAV_fileForm(ModelForm):
    class Meta:
        model = SAV_file
        fields = [field.name for field in model._meta.fields if not (field.name == "creation_date")]    

        error_messages = {
            'sav_file_status': {
                'required': _("Un statut doit etre renseigne."),
            },
            'name_client': {
                'required': _("Le nom du client doit etre renseigne."),
            },
            'street_client': {
                'required': _("La rue du client doit etre renseigne."),
            },
            'city_client': {
                'required': _("La ville du client doit etre renseigne."),
            },
            'zipcode_client': {
                'required': _("Le code postal du client doit etre renseigne."),
            },
            'phone_client': {
                'required': _("Le telephone du client doit etre renseigne."),
            },
            'email_client': {
                'required': _("L'email du client doit etre renseigne."),
            },
            'name_product': {
                'required': _("Le modele du produit doit etre renseigne."),
            },
            'mark_product': {
                'required': _("La marque du produit doit etre renseigne."),
            },
            'serial_number_product': {
                'required': _("Le numero de serie du produit doit etre renseigne."),
            },
        }
    
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [field.name for field in model._meta.fields if not (field.name == "date" or field.name == "refered_SAV_file")]  

class DesignationForm(ModelForm):
    class Meta:
        model = Designation
        fields = [field.name for field in model._meta.fields if not (field.name == "refered_SAV_file")]   




