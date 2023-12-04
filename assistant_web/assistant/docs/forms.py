from django import forms
from .models import File


class UploadFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["file"]


class RenameFileForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ["display_name"]
        labels = {
            "display_name": "New Name",
        }
