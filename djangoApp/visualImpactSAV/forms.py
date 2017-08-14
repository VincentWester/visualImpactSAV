from django.forms import ModelForm
from . import models

class SAV_fileForm(ModelForm):
    class Meta:
        model = models.SAV_file
        fields = [field.name for field in model._meta.fields if not field.name == "creation_date"] 

class SAV_fileUpdateForm(ModelForm):
    class Meta:
        model = models.SAV_file
        fields = [field.name for field in model._meta.fields if not (field.name == "creation_date" or field.name == "file_reference")] 
        

class EventForm(ModelForm):
    class Meta:
        model = models.Event
        fields = [field.name for field in model._meta.fields if not (field.name == "date" or field.name == "refered_SAV_file")]  




