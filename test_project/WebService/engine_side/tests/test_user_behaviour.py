from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.test import Client, TestCase
from django.urls import reverse

class LoginRegisterLogoutTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.logout_url = reverse('logout')
        self.user = {
            'username': 'testuser',
            'password': 'testpass',
            'email': 'testuser@example.com'
        }

    def test_register_user(self):
        response = self.client.post(self.register_url, self.user)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')

    def test_login_user(self):
        User.objects.create_user(**self.user)
        response = self.client.post(self.login_url, self.user, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('test'))
        user = authenticate(username=self.user['username'], password=self.user['password'])
        self.assertEqual(user, self.user)

    def test_logout_user(self):
        User.objects.create_user(**self.user)
        self.client.login(username=self.user['username'], password=self.user['password'])
        response = self.client.get(self.logout_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('info'))
        self.assertFalse(self.user.is_authenticated)