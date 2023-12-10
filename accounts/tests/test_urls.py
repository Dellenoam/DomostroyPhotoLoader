from unittest import TestCase
from django.urls import reverse, resolve
from accounts.views import Login, Logout


class UrlsTestCase(TestCase):
    def test_login_url_is_resolved(self):
        url = reverse('login')
        self.assertEqual(resolve(url).func.__name__, Login.as_view().__name__)

    def test_logout_url_is_resoled(self):
        url = reverse('logout')
        self.assertEqual(resolve(url).func.__name__, Logout.as_view().__name__)
