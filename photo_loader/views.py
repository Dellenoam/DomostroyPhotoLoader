from django.shortcuts import render
from django.views import View
from photo_loader.forms import FileUploadForm
from ftplib import FTP
from io import BytesIO
import base64
import os


# Main page handler
class PhotoLoader(View):

    # Return context and page
    @staticmethod
    def get(request):
        context = dict()
        files_upload_form = FileUploadForm()
        context['files_upload_form'] = files_upload_form
        return render(request, 'photo_loader/photo_loader.html', context)

    # Return files from ftp server
    @staticmethod
    def post(request):
        context = dict()
        files_upload_form = FileUploadForm(request.POST, request.FILES)
        context['files_upload_form'] = files_upload_form

        if files_upload_form.is_valid():
            files = request.FILES.getlist('files')
            user_encoded_files = list()
            server_encoded_files = list()

            ftp = FTP(os.getenv('ftp_server'))
            ftp.login(os.getenv('ftp_username'), os.getenv('ftp_password'))
            # ftp.cwd('DomostroyPhoto/1500x1500')

            for file in files:
                user_encoded_files.append({
                    'data': base64.b64encode(file.read()).decode('utf-8'),
                    'name': file.name

                })

                file_data = BytesIO()
                ftp.retrbinary(f'RETR {file.name}', file_data.write)
                file_data.seek(0)
                server_encoded_files.append({
                    'data': base64.b64encode(file_data.read()).decode('utf-8'),
                    'name': file.name
                })

            ftp.quit()

            context['user_photos'] = user_encoded_files
            context['server_photos'] = server_encoded_files

        return render(request, 'photo_loader/photo_loader.html', context)
