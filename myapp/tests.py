from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser

from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser
from django.contrib.auth.hashers import make_password

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.authtoken.models import Token

from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import CustomUser

class CustomUserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user(self):
        data = {
            'user_name': 'Test User',
            'user_email': 'test@example.com',
            'user_id': 'testuser',
            'user_password': 'testpassword'
        }
        response = self.client.post('/api/user/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_users(self):
        response = self.client.get('/api/user/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_user(self):
        user = CustomUser.objects.create(
            user_name='Test User',
            user_email='test@example.com',
            user_id='testuser',
            user_password='testpassword'
        )
        updated_data = {
            'user_name': 'Updated User',
            'user_email': 'updated@example.com',
            'user_id': 'updateduser',
            'user_password': 'updatedpassword'
        }
        response = self.client.put(f'/api/user/{user.user_id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user(self):
        user = CustomUser.objects.create(
            user_name='Test User',
            user_email='test@example.com',
            user_id='testuser',
            user_password='testpassword'
        )
        response = self.client.delete(f'/api/user/{user.user_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



class UserLoginAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user_data = {
            "user_name": "Test User",
            "user_email": "test@example.com",
            "user_id": "testuser",
            "user_password": "testpassword"
        }
        self.user = CustomUser.objects.create(**self.user_data)

    def test_user_login(self):
        login_data = {
            "user_id": self.user.user_id,
            "user_password": self.user.user_password
        }
        response = self.client.post('/login/', login_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

