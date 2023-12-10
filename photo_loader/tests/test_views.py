import base64
import json

from asgiref.sync import async_to_sync
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from photo_loader.forms import FilesUploadForm
from photo_loader.ftp_hanlders import FTPImagesProcessor


class ViewsTestCase(TestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)

        self.files = [
            {'file_name': 'ИЖ450.jpg', 'file_data': b'test_file_data'},
            {'file_name': 'test_file_not_found', 'file_data': b'test_file_not_found_data'}
        ]

        self.ftp = FTPImagesProcessor()

    @async_to_sync
    async def ftp_test_file_upload(self):
        await self.ftp.login()

        async with self.ftp.client.upload_stream(self.files[0]['file_name']) as stream:
            await stream.write(self.files[0]['file_data'])

        await self.ftp.client.quit()

    @async_to_sync
    async def ftp_test_file_delete(self):
        await self.ftp.login()

        await self.ftp.client.remove(self.files[0]['file_name'])

        await self.ftp.client.quit()

    def test_home_get_method(self):
        url = reverse('home')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'photo_loader/home.html')

    def test_photo_loader_get_method_authenticated(self):
        self.client.login(username=self.username, password=self.password)

        url = reverse('photo_loader')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'photo_loader/photo_loader.html')

        self.assertIn('files_upload_form', response.context)
        self.assertIsInstance(response.context['files_upload_form'], FilesUploadForm)

    def test_photo_loader_get_method_not_authenticated(self):
        url = reverse('photo_loader')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

    def test_photo_loader_post_method_authenticated_valid(self):
        self.client.login(username=self.username, password=self.password)

        self.ftp_test_file_upload()

        url = reverse('photo_loader')
        data_files = []
        for file in self.files:
            data_files.append(SimpleUploadedFile(file['file_name'], file['file_data']))
        response = self.client.post(url, {'files': data_files})

        self.assertEqual(response.status_code, 200)

        self.assertIn('files_upload_form', response.context)
        self.assertIsInstance(response.context['files_upload_form'], FilesUploadForm)

        self.assertIn('files_selection_form', response.context)
        self.assertEqual(response.context['files_selection_form'], True)

        self.assertIn('user_photos', response.context)
        self.assertEqual(response.context['user_photos'][0]['name'], self.files[0]['file_name'])
        self.assertEqual(response.context['user_photos'][1]['name'], self.files[1]['file_name'])
        self.assertEqual(response.context['user_photos'][0]['data'],
                         base64.b64encode(self.files[0]['file_data']).decode('utf-8'))
        self.assertEqual(response.context['user_photos'][1]['data'],
                         base64.b64encode(self.files[1]['file_data']).decode('utf-8'))

        self.assertIn('server_photos', response.context)
        self.assertEqual(response.context['server_photos'][0]['name'], self.files[0]['file_name'])
        self.assertEqual(response.context['server_photos'][1]['name'], self.files[1]['file_name'])
        self.assertEqual(response.context['server_photos'][0]['data'],
                         base64.b64encode(self.files[0]['file_data']).decode('utf-8'))
        with open('media/server_media/404.jpg', 'rb') as image_404:
            self.assertEqual(response.context['server_photos'][1]['data'],
                             base64.b64encode(image_404.read()).decode('utf-8'))

        self.assertIn('not_found', response.context['server_photos'][1])
        self.assertEqual(response.context['server_photos'][1]['not_found'], '(Не найден на сервере)')

        self.assertIn('product_names', response.context)
        self.assertNotEqual(response.context['product_names'][0], 'Название товара не найдено')
        self.assertEqual(response.context['product_names'][1], 'Название товара не найдено')

        self.ftp_test_file_delete()

    def test_photo_loader_post_method_authenticated_not_valid(self):
        self.client.login(username=self.username, password=self.password)

        url = reverse('photo_loader')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 400)

    def test_photo_loader_post_method_not_authenticated(self):
        url = reverse('photo_loader')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))

    def test_photo_loader_submit_post_method_authorized_valid(self):
        self.client.login(username=self.username, password=self.password)

        self.ftp_test_file_upload()

        url = reverse('photo_loader_submit')
        response = self.client.post(url, json.dumps({
            'file_name': self.files[0]['file_name'],
            'file_data': base64.b64encode(self.files[0]['file_data']).decode('utf-8')
        }), content_type='application/json')

        self.assertEqual(response.status_code, 204)

        self.ftp_test_file_delete()

    def test_photo_loader_submit_post_method_authorized_not_valid(self):
        self.client.login(username=self.username, password=self.password)

        url = reverse('photo_loader_submit')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 400)

    def test_photo_loader_submit_method_post_not_authorized(self):
        url = reverse('photo_loader_submit')
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('login'))
