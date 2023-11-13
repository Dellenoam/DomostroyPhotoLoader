import asyncio
import json
import re
import traceback
import aioftp
import aiohttp
import logging
from django.utils.decorators import method_decorator
from photo_loader.decorators import async_login_required
from photo_loader.ftp_hanlders import FTPImagesProcessor
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from photo_loader.forms import FileUploadForm

logger = logging.getLogger(__name__)


class Home(View):
    """
    Default home page
    """

    def get(self, request):
        return render(request, 'photo_loader/home.html')


@method_decorator(async_login_required, name='dispatch')
class PhotoLoader(View):
    """
    Manages the photo loading view, which involves displaying the form for file uploads
    and processing the uploaded files.

    GET method returns a page with the file upload form.

    POST method handles requests for the photo loader view, processes the uploaded files,
    and displays the selection form.
    """

    # Return context and page
    async def get(self, request):
        context = dict()
        files_upload_form = FileUploadForm()
        context['files_upload_form'] = files_upload_form
        return render(request, 'photo_loader/photo_loader.html', context)

    # Return files from ftp server
    async def post(self, request):
        context = dict()
        files_upload_form = FileUploadForm(request.POST, request.FILES)
        context['files_upload_form'] = files_upload_form
        context['files_selection_form'] = False

        if files_upload_form.is_valid():
            files = request.FILES.getlist('files')

            ftp_processor = FTPImagesProcessor()

            try:
                user_encoded_files, server_encoded_files, product_names = await ftp_processor.get_files_from_server(
                    files
                )
            except Exception as e:
                return handle_error(e)

            context['user_photos'] = user_encoded_files[::-1]
            context['server_photos'] = server_encoded_files[::-1]
            context['product_names'] = product_names[::-1]
            context['files_selection_form'] = True

        return render(request, 'photo_loader/photo_loader.html', context)


@method_decorator(async_login_required, name='dispatch')
class PhotoLoaderSubmit(View):
    """
    View for handling photo loader submissions.

    GET method redirects to the 'photo_loader' page.

    POST method processes JSON data from the request body, decodes it,
    and asynchronously replaces files using FTPImagesProcessor.
    """

    # Replacing files on ftp server
    async def post(self, request):
        data = json.loads(request.body.decode('utf-8'))
        ftp = FTPImagesProcessor()
        await asyncio.create_task(ftp.replace_files(data))

        return HttpResponse(status=200)


def handle_error(exception):
    """
    Handles errors and returns an appropriate HTTP response.

    :param exception: The exception to handle
    :return: HTTP response with an error message.
    """
    trace = traceback.extract_tb(exception.__traceback__)

    error_messages = {
        TimeoutError: 'Не удалось подключиться к серверу',
        aioftp.errors.StatusCodeError: {
            '530': 'Не удалось авторизоваться на сервере',
            '550': 'Не удалось получить нужную папку или файл',
        },
        ConnectionRefusedError: 'Сервер отказал в соединении или не слушает указанный порт',
        aiohttp.ClientResponseError: 'Ошибка при выполнении запроса',
    }

    unknown_error_message = 'Неизвестная ошибка'

    if type(exception) in error_messages:
        message = error_messages[type(exception)]

        if isinstance(message, dict):
            match = re.search(r'got (\d+)', str(exception))
            if match:
                error_code = match.group(1)
                message = message.get(error_code, unknown_error_message)

                if message == 'Неизвестная ошибка':
                    logger.error(f'Type: {type(exception)} - {exception} - {trace[0]} - {trace[1]}')
                    return HttpResponse(
                        'Неизвестная ошибка <br> <a href="javascript:history.back()">Назад</a>',
                        status=500
                    )

        logger.warning(f'\n{type(exception)} - {exception} - {trace[0]} - {trace[1]}')
        return HttpResponse(f'{message} <br> <a href="javascript:history.back()">Назад</a>')

    logger.error(f'Type: {type(exception)} - {exception} - {trace[0]} - {trace[1]}')
    return HttpResponse(f'{unknown_error_message} <br> <a href="javascript:history.back()">Назад</a>', status=500)
