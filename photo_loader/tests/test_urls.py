from django.test import TestCase
from django.urls import reverse, resolve
from photo_loader.views import Home, PhotoLoader, PhotoLoaderSubmit


class UrlsTestCase(TestCase):
    def test_home_is_resolved(self):
        url = reverse('home')
        self.assertEqual(resolve(url).func.__name__, Home.as_view().__name__)

    def test_photo_loader_is_resolved(self):
        url = reverse('photo_loader')
        self.assertEqual(resolve(url).func.__name__, PhotoLoader.as_view().__name__)

    def test_photo_loader_submit_is_resolved(self):
        url = reverse('photo_loader_submit')
        self.assertEqual(resolve(url).func.__name__, PhotoLoaderSubmit.as_view().__name__)
