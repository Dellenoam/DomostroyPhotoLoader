from django import forms


class FilesInput(forms.ClearableFileInput):
    template_name = 'photo_loader/files_input.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['multiple'] = True
        return context
