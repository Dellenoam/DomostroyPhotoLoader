from django.shortcuts import render
from django.views import View
from photo_loader.forms import FileUploadForm
import base64


# Main page handler
class PhotoLoader(View):
    # Return context and page
    @staticmethod
    def get(request):
        context = dict()
        files_upload_form = FileUploadForm()
        context['files_upload_form'] = files_upload_form
        return render(request, 'photo_loader/photo_loader.html', context)

    @staticmethod
    def post(request):
        context = dict()
        files_upload_form = FileUploadForm(request.POST, request.FILES)
        context['files_upload_form'] = files_upload_form

        if files_upload_form.is_valid():
            files = request.FILES.getlist('files')
            encoded_files = list()

            for file in files:
                encoded_file = {'data': base64.b64encode(file.read()).decode('utf-8')}
                encoded_file.update({'name': file.name})
                encoded_files.append(encoded_file)

            context['user_photos'] = encoded_files
        else:
            print(files_upload_form.errors)

        return render(request, 'photo_loader/photo_loader.html', context)
