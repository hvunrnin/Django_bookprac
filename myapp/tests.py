# from django.test import TestCase
# from rest_framework.test import APIClient
# from rest_framework import status
# from .models import CustomUser

# from django.urls import reverse
# from rest_framework.test import APIClient
# from rest_framework import status
# from .models import CustomUser
# from django.contrib.auth.hashers import make_password

# from django.test import TestCase
# from rest_framework.test import APIClient
# from rest_framework import status
# from .models import CustomUser
# from .serializers import CustomUserSerializer
# from rest_framework.authtoken.models import Token

# from django.test import TestCase
# from rest_framework.test import APIClient
# from rest_framework import status
# from .models import CustomUser

# class CustomUserAPITest(TestCase):
#     def setUp(self):
#         self.client = APIClient()

#     def test_create_user(self):
#         data = {
#             'user_name': 'Test User',
#             'user_email': 'test@example.com',
#             'user_id': 'testuser',
#             'user_password': 'testpassword'
#         }
#         response = self.client.post('/api/user/', data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_201_CREATED)

#     def test_get_users(self):
#         response = self.client.get('/api/user/')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_update_user(self):
#         user = CustomUser.objects.create(
#             user_name='Test User',
#             user_email='test@example.com',
#             user_id='testuser',
#             user_password='testpassword'
#         )
#         updated_data = {
#             'user_name': 'Updated User',
#             'user_email': 'updated@example.com',
#             'user_id': 'updateduser',
#             'user_password': 'updatedpassword'
#         }
#         response = self.client.put(f'/api/user/{user.user_id}/', updated_data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

#     def test_delete_user(self):
#         user = CustomUser.objects.create(
#             user_name='Test User',
#             user_email='test@example.com',
#             user_id='testuser',
#             user_password='testpassword'
#         )
#         response = self.client.delete(f'/api/user/{user.user_id}/')
#         self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)



# class UserLoginAPITest(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.user_data = {
#             "user_name": "Test User",
#             "user_email": "test@example.com",
#             "user_id": "testuser",
#             "user_password": "testpassword"
#         }
#         self.user = CustomUser.objects.create(**self.user_data)

#     def test_user_login(self):
#         login_data = {
#             "user_id": self.user.user_id,
#             "user_password": self.user.user_password
#         }
#         response = self.client.post('/login/', login_data)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)

import requests

# 아래 URL을 'http://localhost:8000/'와 같이 적절하게 수정해야 합니다.
base_url = 'http://localhost:8000/'

# 검색할 책 이름을 입력합니다.
query = 'Python Programming'

# GET 요청을 보내는 함수
def test_get_book_search():
    url = f"{base_url}search/{query}/"
    response = requests.get(url)
    print(response.json())

# POST 요청을 보내는 함수
def test_post_user_book():
    url = f"{base_url}add/{query}/"
    user_id = 1  # 예시로 사용자 ID를 지정
    state = 'to_read'  # 사용자가 선택한 상태
    data = {
        'user_id': user_id,
        'state': state
    }
    response = requests.post(url, data=data)
    print(response.json())

if __name__ == '__main__':
    test_get_book_search()
    test_post_user_book()
