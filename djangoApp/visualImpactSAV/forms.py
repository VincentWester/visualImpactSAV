from django.forms import ModelForm
from .models import SAV_file, Event, Pdf_generation_file

class SAV_fileForm(ModelForm):
    class Meta:
        model = SAV_file
        fields = [field.name for field in model._meta.fields if not (field.name == "creation_date" or field.name == "tracking_number" or field.name == "file_reference")]         

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = [field.name for field in model._meta.fields if not (field.name == "date" or field.name == "refered_SAV_file")]  

class Pdf_generation_file_form(ModelForm):
    class Meta:
        model = Pdf_generation_file
        fields = ["filename"]  




