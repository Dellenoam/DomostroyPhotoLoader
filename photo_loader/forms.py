from django import forms
from photo_loader.widgets import FilesInput


class FilesUploadForm(forms.Form):
    files = forms.FileField(widget=FilesInput)
