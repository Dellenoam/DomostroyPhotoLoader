from django import forms
from photo_loader.widgets import FilesInput


class FileUploadForm(forms.Form):
    files = forms.FileField(widget=FilesInput)
