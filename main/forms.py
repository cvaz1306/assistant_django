from django import forms
from .models import *
#Unnecessary.
class UploadFileForm(forms.ModelForm):
    class Meta:
        model = UploadedFile
        fields = ['file']