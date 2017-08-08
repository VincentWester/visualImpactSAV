from django.forms import ModelForm
from . import models

class SAV_fileForm(ModelForm):
    class Meta:
        model = models.SAV_file
        fields = [field.name for field in model._meta.fields if not field.name == "creation_date"] 
        

class EventForm(ModelForm):
    class Meta:
        model = models.Event
        fields = "__all__" 




