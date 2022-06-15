from django.conf import settings
from django.test import TestCase

from authapp.models import User
from django.test.client import Client


class UserTestCase(TestCase):

    def setUp(self) -> None:
        self.user_name = 'test_user'
        self.email = 'test@mail.ru'
        self.password = 'test@mail.rutest@mail.ru'

        self.new_user_data = {
            'username': 'test_some_user',
            'first_name': 'test_some_user1',
            'last_name': 'test_some_user2',
            'email': 'test_some_user@mail.ru',
            'password1': 'test_some_user@mail.rutest_some_user@mail.ru',
            'password2': 'test_some_user@mail.rutest_some_user@mail.ru',
            'age': 31
        }

        self.user = User.objects.create_superuser(self.user_name, self.email, self.password)
        self.client = Client()

    def test_login(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        response = self.client.get(f'/authapp/profile/{self.user.pk}')
        self.assertEqual(response.status_code, 302)

        self.client.login(username=self.user_name, password=self.password)
        response = self.client.get(f'/authapp/profile/{self.user.pk}')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.post('/authapp/register', data=self.new_user_data)
        self.assertEqual(response.status_code, 200)

        user = User.objects.get(username=self.new_user_data['username'])

        activation_url = f'{settings.DOMAIN_NAME}/authapp/verify/{user.email}/{user.activation_key}/'
        response = self.client.get(activation_url)
        self.assertEqual(response.status_code, 200)
        # self.assertFalse(self.user.is_active)
        # self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)


    def tearDown(self) -> None:
        pass
