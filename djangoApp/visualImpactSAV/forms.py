from django.forms import ModelForm
from .models import SAV_file, Event, Pdf_client_invoice_file

class SAV_fileForm(ModelForm):
    class Meta:
        model = SAV_file
        fields = [field.name for field in model._meta.fields if not field.name == "creation_date"] 

class SAV_fileUpdateForm(ModelForm):
    class Meta:
        model = SAV_file
        fields = [field.name for field in model._meta.fields if not (field.name == "creation_date" or field.name == "file_reference")]         

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [field.name for field in model._meta.fields if not (field.name == "date" or field.name == "refered_SAV_file")]  

class Pdf_client_invoice_file_form(ModelForm):
    class Meta:
        model = Pdf_client_invoice_file
        fields = ["filename"]  




