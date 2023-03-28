from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class RegisterUserTestCase(TestCase):
    def test_register_user_success(self):
        """
        Test registering a user with valid form data.
        """
        url = reverse('register_user')
        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(url, data)
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='testuser').exists())

    def test_register_user_failure(self):
        """
        Test registering a user with invalid form data.
        """
        url = reverse('register_user')
        data = {
            'username': '',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required.')
        self.assertFalse(User.objects.filter(username='').exists())

    def test_register_user_db_failure(self):
        """
        Test registering a user when the database save fails.
        """
        url = reverse('register_user')
        data = {
            'username': 'testuser',
            'password1': 'testpassword',
            'password2': 'testpassword',
        }
        with self.assertRaises(Exception):
            # Force the database save to fail by causing an exception in the User model's save method
            with self.settings(USER_MODEL='myapp.tests.test_models.FailingUser'):
                self.client.post(url, data)
        self.assertFalse(User.objects.filter(username='testuser').exists())
