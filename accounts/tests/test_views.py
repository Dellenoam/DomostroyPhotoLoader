from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from accounts.forms import LoginForm


class ViewsTestCase(TestCase):
    def setUp(self):
        self.login_url = reverse('login')

        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = get_user_model().objects.create_user(username=self.username, password=self.password)

    def test_login_get_method(self):
        response = self.client.get(self.login_url)

        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'accounts/login.html')

        self.assertIn('login_form', response.context)
        self.assertIsInstance(response.context['login_form'], LoginForm)

    def test_login_post_method_valid(self):
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(response.url, reverse('photo_loader'))

        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_post_method_valid_with_next(self):
        next_url = reverse('photo_loader')
        data = {'username': self.username, 'password': self.password}
        response = self.client.post(f'{self.login_url}?next={next_url}', data)

        self.assertEqual(response.status_code, 302)

        self.assertEqual(response.url, next_url)

        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_login_post_method_not_valid(self):
        data = {'username': 'fakeuser', 'password': 'fakepassword'}
        response = self.client.post(self.login_url, data)

        self.assertEqual(response.status_code, 400)

        self.assertTemplateUsed(response, 'accounts/login.html')

        self.assertIn('login_form', response.context)
        self.assertIsInstance(response.context['login_form'], LoginForm)
