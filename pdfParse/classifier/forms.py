from django import forms
from .models import *
class UploadFileForm(forms.ModelForm):
    # file = forms.FileField()
    class Meta:
        model = pdf
        fields = ('file',)