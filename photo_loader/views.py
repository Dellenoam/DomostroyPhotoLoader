import json
import re
import aioftp
import aiohttp
from photo_loader import services
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from photo_loader.forms import FileUploadForm


# Main page handler
class PhotoLoader(View):
    # Return context and page
    @staticmethod
    async def get(request):
        context = dict()
        files_upload_form = FileUploadForm()
        context['files_upload_form'] = files_upload_form
        return render(request, 'photo_loader/photo_loader.html', context)

    # Return files from ftp server
    @staticmethod
    async def post(request):
        context = dict()
        files_upload_form = FileUploadForm(request.POST, request.FILES)
        context['files_upload_form'] = files_upload_form
        context['files_selection_form'] = False

        if files_upload_form.is_valid():
            files = request.FILES.getlist('files')

            try:
                ftp = await services.ftp_login()
            except Exception as e:
                return handle_error(e)

            try:
                user_encoded_files, server_encoded_files, product_names = await services.ftp_images_handling(ftp, files)
            except Exception as e:
                return handle_error(e)

            context['user_photos'] = user_encoded_files[::-1]
            context['server_photos'] = server_encoded_files[::-1]
            context['product_names'] = product_names[::-1]
            context['files_selection_form'] = True

        return render(request, 'photo_loader/photo_loader.html', context)


class PhotoLoaderSubmit(View):
    @staticmethod
    def get(request):
        return redirect('photo_loader')

    @staticmethod
    def post(request):
        data = json.loads(request.body.decode('utf-8'))
        print(data['file_name'])
        return JsonResponse({'message': 'Данные получены!'})


def handle_error(exception):
    error_messages = {
        TimeoutError: 'Не удалось подключиться к серверу',
        aioftp.errors.StatusCodeError: {
            '530': 'Не удалось авторизоваться на сервере',
            '550': 'Не удалось получить нужную папку или файл',
        },
        ConnectionRefusedError: 'Сервер отказал в соединении или не слушает указанный порт',
        aiohttp.ClientResponseError: 'Ошибка при выполнении запроса к API',
        KeyError: 'В данных JSON отсутствует искомый элемент',
    }

    if type(exception) in error_messages:
        message = error_messages[type(exception)]

        if isinstance(message, dict):
            match = re.search(r'got (\d+)', str(exception))
            if match:
                error_code = match.group(1)
                message = message.get(error_code, 'Неизвестная ошибка')

        return HttpResponse(f'{message} <br> <a href="javascript:history.back()">Назад</a>')

    return HttpResponse('Неизвестная ошибка <br> <a href="javascript:history.back()">Назад</a>')
