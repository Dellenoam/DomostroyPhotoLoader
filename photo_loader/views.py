from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from photo_loader.forms import FileUploadForm
from ftplib import FTP, error_perm
from io import BytesIO
import base64
import os
import requests


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
            products_name = list()

            try:
                ftp = FTP(os.getenv('ftp_server'))
                ftp.login(os.getenv('ftp_username'), os.getenv('ftp_password'))
                ftp.cwd('DomostroyPhoto/1500x1500')
            except TimeoutError:
                return HttpResponse('Не удалось подключиться к серверу <br>'
                                    '<a href="javascript:history.back()">Назад</a>')
            except error_perm as exception:
                if '530' in str(exception):
                    return HttpResponse('Не удалось авторизоваться на сервере <br>'
                                        '<a href="javascript:history.back()">Назад</a>')
                elif '550' in str(exception):
                    return HttpResponse('Не удалось открыть папку или файл <br>'
                                        '<a href="javascript:history.back()">Назад</a>')
                else:
                    return HttpResponse('Неизвестная ошибка <br>'
                                        '<a href="javascript:history.back()">Назад</a>')
            except ConnectionRefusedError:
                return HttpResponse('Сервер отказал в соединении или не слушает указанный порт <br>'
                                    '<a href="javascript:history.back()">Назад</a>')

        for file in files:
            user_encoded_files.append({
                'data': base64.b64encode(file.read()).decode('utf-8'),
                'name': file.name
            })

            file_data = BytesIO()

            try:
                ftp.retrbinary(f'RETR {file.name}', file_data.write)
                file_data.seek(0)
                server_encoded_files.append({
                    'data': base64.b64encode(file_data.read()).decode('utf-8'),
                    'name': file.name
                })
            except error_perm as exception:
                if '550' in str(exception):
                    with open('media/server_media/404.jpg', 'rb') as image_404:
                        server_encoded_files.append({
                            'data': base64.b64encode(image_404.read()).decode('utf-8'),
                            'name': file.name
                        })
                else:
                    return HttpResponse('Неизвестная ошибка <br>'
                                        '<a href="javascript:history.back()">Назад</a>')

            # Split the file name by '.' and '_' to extract its base name
            try:
                base_file_name = file.name.split('.')[0].split('_')[0]
                vendor_code = base_file_name
                domostroy_api_key = os.getenv('domostroy_api_key')
                domostroy_response = requests.get(
                    f'https://sort.diginetica.net/search?st={vendor_code}'
                    f'&apiKey={domostroy_api_key}'
                    f'&fullData=true&withSku=true').json()
                if domostroy_response['products'][0]['attributes']['артикул'][0] != base_file_name:
                    products_name.append('Название товара не найдено')
                else:
                    products_name.append(domostroy_response['products'][0]['name'])
            except IndexError:
                return HttpResponse('В названии файла отсутствует расширение <br>'
                                    '<a href="javascript:history.back()">Назад</a>')
            except requests.RequestException:
                return HttpResponse('Не удалось получить ответ от API <br>'
                                    '<a href="javascript:history.back()">Назад</a>')
            except KeyError:
                return HttpResponse('В данных JSON отсутствует искомый элемент <br>'
                                    '<a href="javascript:history.back()">Назад</a>')

        ftp.quit()

        context['user_photos'] = user_encoded_files[::-1]
        context['server_photos'] = server_encoded_files[::-1]
        context['products_name'] = products_name[::-1]

        return render(request, 'photo_loader/photo_loader.html', context)
