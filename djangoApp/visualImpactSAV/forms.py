# coding: utf-8

from django.contrib.auth.models import User
from django.forms import ModelForm, CharField, EmailField, PasswordInput, ValidationError, ModelChoiceField
from .models import SAV_file, SAV_file_status, Event, Designation, Guarantee, Furnisher
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from django.utils.translation import ugettext_lazy as _

class SignUpForm(UserCreationForm):
    email = EmailField(max_length=254, help_text='Obligatoire. Veuillez indiquer une adresse mail valide.')    
    
    def __init__(self, *args, **kwargs):
        super(UserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = _('Obligatoire. Inscrivez votre nom d\'utilisateur.')
        self.fields['username'].label = _('Nom d\'utilisateur')
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
                'required': _("Le mot de passe n'a pas ete recopie."),
            },
        }

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class SAV_fileForm(ModelForm):
    furnisher = ModelChoiceField(queryset = Furnisher.objects.all(), empty_label = "---", required = False)
    sav_file_status = ModelChoiceField(queryset = SAV_file_status.objects.all(), required = False)

    class Meta:
        model = SAV_file
        fields = [field.name for field in model._meta.fields if not (field.name == "creation_date" or field.name == "registred_by")]    

        error_messages = {
            'name_client': {
                'required': _("Le nom du client doit etre renseigné."),
            },
            'street_client': {
                'required': _("La rue du client doit etre renseigné."),
            },
            'city_client': {
                'required': _("La ville du client doit etre renseigné."),
            },
            'zipcode_client': {
                'required': _("Le code postal du client doit etre renseigné."),
            },
            'phone_client': {
                'required': _("Le téléphone du client doit etre renseigné."),
            },
            'email_client': {
                'required': _("L'email du client doit etre renseigné."),
            },
            'name_product': {
                'required': _("Le modèle du produit doit etre renseigné."),
            },
            'mark_product': {
                'required': _("La marque du produit doit etre renseigné."),
            },
            'serial_number_product': {
                'required': _("Le numéro de serie du produit doit etre renseigné."),
            },
            'guarantee': {
                'required': _("Le statut de garantie du produit doit etre renseigné."),
            },
        }
    
class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [field.name for field in model._meta.fields if not (field.name == "date" or field.name == "refered_SAV_file")]
        labels = {
            "title": "Titre",
            "action": "Action",
        }

class DesignationForm(ModelForm):
    class Meta:
        model = Designation
        fields = [field.name for field in model._meta.fields if not (field.name == "refered_SAV_file")]  
        labels = {
            "designation": "Désignation",
            "quantity": "Quantité",
            "price": "Prix",
        } 

class GuaranteeForm(ModelForm):
    class Meta:
        model = Guarantee
        fields = [field.name for field in model._meta.fields]   
        labels = {
            "mark": "Marque",
            "complements": "Informations supplémentaires",
            "guarantee_time": "Temps de garantie",
            "procedure": "Procédure",
        }

class FurnisherForm(ModelForm):
    class Meta:
        model = Furnisher
        fields = [field.name for field in model._meta.fields] 
        labels = {
            "mark": "Marque",
            "street": "Rue",
            "complements": "Compléments",
            "zipcode": "Code postal",
            "city": "Ville",
            "phone": "Téléphone",
            "commentary": "Commentaire",
        }

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = []




