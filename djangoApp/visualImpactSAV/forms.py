from django.contrib.auth.models import User
from django.forms import ModelForm, CharField, EmailField, PasswordInput, ValidationError
from .models import SAV_file, Event, Designation, Guarantee
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

class SignUpForm(UserCreationForm):
    email = EmailField(max_length=254, help_text='Obligatoire. Veuillez indiquer une adresse mail valide.')    
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = _('Obligatoire. Inscrivez votre nom d\'utilisateur.')
        self.fields['username'].label = _('Nom d\'utilisateur.')
        self.fields['password1'].help_text = _('Obligatoire. Veuillez indiquer votre mot de passe.')
        self.fields['password1'].label = _('Mot de passe')
        self.fields['password2'].help_text = _('Obligatoire. Verification du mot de passe : retapez votre mot de passe.')
        self.fields['password2'].label = _('Confirmation')

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

        error_messages = {
            'username': {
                'required': _("Un nom d'utilisateur doit etre renseigne."),
            },
            'email': {
                'required': _("Un email doit etre renseigne."),
            },
            'password1': {
                'required': _("Un mot de passe doit etre renseigne."),
            },
            'password2': {
                'required': _("Le mot de passe n'a pas ete recopie"),
            },
        }

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class SAV_fileForm(ModelForm):
    class Meta:
        model = SAV_file
        fields = [field.name for field in model._meta.fields if not (field.name == "creation_date" or field.name == "registred_by")]    

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
            'guarantee': {
                'required': _("Le statut de garantie du produit doit etre renseigne."),
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

class GuaranteeForm(ModelForm):
    class Meta:
        model = Guarantee
        fields = [field.name for field in model._meta.fields]   

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = []




