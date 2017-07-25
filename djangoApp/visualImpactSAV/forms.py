from django.forms import ModelForm
from . import models

class SAV_fileForm(ModelForm):
    class Meta:
        model = models.SAV_file
        fields = ('file_reference',)  
        

class EventForm(ModelForm):
    class Meta:
        model = models.Event
        fields = "__all__" 