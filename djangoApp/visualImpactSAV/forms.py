from django.forms import ModelForm
from . import models

class SAV_fileForm(ModelForm):
    class Meta:
        model = models.SAV_file
        fields = "__all__"  
        

class EventForm(ModelForm):
    class Meta:
        model = models.Event
        fields = "__all__" 




