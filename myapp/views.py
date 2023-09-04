from django.shortcuts import render, redirect
from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import CustomUser, Book, UserBook
from .serializers import CustomUserSerializer, BookSerializer, UserBookSerializer
from rest_framework.generics import ListAPIView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import urllib.request
import urllib.parse
import json
from rest_framework.views import APIView
import os
import sys
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token

from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import check_password
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission

# class NoAuthentication(BaseAuthentication):
#     def authenticate(self, request):
#         return None  # 인증을 비활성화하기 위해 None을 반환

# class NoPermission(BasePermission):
#     def has_permission(self, request, view):
#         return True  # 권한을 비활성화하기 위해 항상 True 반환


# Create your views here.
class CustomUserview(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

class Bookview(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class UserBookview(viewsets.ModelViewSet):
    queryset = UserBook.objects.all()
    serializer_class = UserBookSerializer

@api_view()
def hello_drf(request):
    return Response({'message':'hello'})

def main(request):
    return render(request, 'home.html')

def createForm(request):
    return render(request, 'create.html')

def createUser(request):
    userContent_id = request.POST['id']  # Corrected to match HTML input name attribute
    userContent_password = request.POST['password']  # Corrected to match HTML input name attribute
    userContent_name = request.POST['name']  # Corrected to match HTML input name attribute
    userContent_email = request.POST['email']  # Corrected to match HTML input name attribute
    
    user = CustomUser(user_id=userContent_id, user_password=userContent_password, user_name=userContent_name, user_email=userContent_email)
    user.save()

    return HttpResponseRedirect(reverse('main'))

def loginForm(request):
    return render(request, 'login.html')

from django.core.cache import cache

def custom_login(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(user_id=userid)
        except CustomUser.DoesNotExist:
            user = None

        if user and user.user_password == password:
            login(request, user)
            user_info={'user_id': user.user_id}
            lists_user = UserBook.objects.filter(user=user)
            lists_all = Book.objects.all()  # Book 객체 목록을 가져옴
            data = {'lists_user': lists_user, 'lists_all': lists_all,'user_info': user_info}
            request.session['user_id'] = user.user_id 
            cache.set(f'user_data_{user.user_id}', data, timeout=None)
            #return redirect('mybooks') 
            return render(request, 'mybooks.html', data)
        else:
            return HttpResponseRedirect(reverse('main'))  # 로그인 실패 시 메인 페이지로 이동
    else:
        return HttpResponse("")
    
        

def custom_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main'))

def test(request):
    lists = Book.objects.all()
    data = {'lists':lists} 
    return render(request, 'mybooks.html', data)


def add_user_book(request):
    user_id = request.POST.get('user_id')
    book_id = request.POST.get('book_id')

    try:
        user = CustomUser.objects.get(id=user_id)
        book = Book.objects.get(id=book_id)
    except CustomUser.DoesNotExist or Book.DoesNotExist:
        return HttpResponseRedirect(reverse('main'))

    # 이미 추가한 책인지 확인
    if UserBook.objects.filter(user=user, title=book.title).exists():
        return HttpResponseRedirect(reverse('main'))  # 이미 추가한 책인 경우 메인 페이지로 이동

    user_book = UserBook.objects.create(
        user=user,
        title=book.title,
        author=book.author,
        publication_year=book.publication_year,
        genre=book.genre,
        publisher=book.publisher,
        state=UserBook.TO_READ,  # 적절한 상태 선택
    )

    return redirect('loginForm')

def delete_user_book(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        book_id = request.POST.get('book_id')

        try:
            user = CustomUser.objects.get(id=user_id)
            user_book = get_object_or_404(UserBook, user=user, id=book_id)
            user_book.delete()
        except CustomUser.DoesNotExist or UserBook.DoesNotExist:
            pass

    #return redirect('mybooks')
    #return redirect(request.META.get('HTTP_REFERER'))
    return redirect('loginForm')

def mybooks(request):
    user_id = request.session.get('user_id')  # 세션에서 사용자 정보 가져오기

    if user_id:
        try:
            user = CustomUser.objects.get(user_id=user_id)
            lists_user = UserBook.objects.filter(user=user)
            lists_all = Book.objects.all()
            user_info = {'user_id': user.user_id}
            data = {'lists_user': lists_user, 'lists_all': lists_all, 'user_info': user_info}
            return render(request, 'mybooks.html', data)
        except CustomUser.DoesNotExist:
            return HttpResponseRedirect(reverse('main'))
    else:
        return HttpResponseRedirect(reverse('main'))


#book api 
def api_book_search1(request):

    if request.method == 'GET':
        # config_secret_debug = json.loads(open(settings.SECRET_DEBUG_FILE).read())
        # client_id = config_secret_debug['NAVER']['CLIENT_ID']
        # client_secret = config_secret_debug['NAVER']['CLIENT_SECRET']

        client_id = "71GX1MGulezdAHHJXWQk"
        client_secret = "IJlwpjxdQk"
        #query = request.GET.get('q', '')  # 검색어 가져오기
        encText = urllib.parse.quote("파이썬")
        url = "https://openapi.naver.com/v1/search/book?query=" + encText  # json 결과
        book_api_request = urllib.request.Request(url)
        book_api_request.add_header("X-Naver-Client-Id",client_id)
        book_api_request.add_header("X-Naver-Client-Secret",client_secret)
        response = urllib.request.urlopen(book_api_request)
        rescode = response.getcode()
        if (rescode == 200):
            response_body = response.read()
            result = json.loads(response_body.decode('utf-8'))
            items = result.get('items')

            context = {
                'items': items
            }
            return render(request, 'home.html', context=context)
    else:
        return render(request, 'home.html')

from rest_framework.permissions import IsAuthenticatedOrReadOnly



class User(APIView):
    # authentication_classes = [NoAuthentication]
    # permission_classes = [NoPermission]

    def post(self, request): #회원 생성
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, user_id=None):  # user_id를 매개변수로 받음
        if user_id is None:  # user_id가 주어지지 않은 경우 (리스트 가져오기)
            users = CustomUser.objects.all()
            serializer = CustomUserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # user_id가 주어진 경우 (특정 사용자 조회)
        try:
            user = CustomUser.objects.get(user_id=user_id)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, user_id): #회원 수정
        try:
            user = CustomUser.objects.get(user_id=user_id)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomUserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, user_id): #회원 삭제
        try:
            user = CustomUser.objects.get(user_id=user_id)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def test_get(self, request): #리스트 가져오기
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

@api_view(['GET'])
def get_detail(self, request, user_id): #특정 사용자 조회
        try:
            user = CustomUser.objects.get(user_id=user_id)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserLogin(APIView):
    # authentication_classes = [NoAuthentication]
    # permission_classes = [NoPermission]
    def get(self, request, user_id=None):  # user_id를 매개변수로 받음
        if user_id is None:  # user_id가 주어지지 않은 경우 (리스트 가져오기)
            users = CustomUser.objects.all()
            serializer = CustomUserSerializer(users, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # user_id가 주어진 경우 (특정 사용자 조회)
        try:
            user = CustomUser.objects.get(user_id=user_id)
        except CustomUser.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def post(self, request):
        userid = request.data.get('user_id')
        password = request.data.get('user_password')
        
        # try:
        #     user = CustomUser.objects.get(user_id=userid)
        #     if check_password(password, user.user_password):
        #         response_data = {'message': 'Login successful', 'user_id': user.id}
        #         return Response(response_data, status=status.HTTP_200_OK)
        #     else:
        #         return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        # except CustomUser.DoesNotExist:
        #     return Response({'error': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            user = CustomUser.objects.get(user_id=userid)
            if user and user.user_password == password:
                response_data = {'message': 'Login successful', 'user_id': user.id}
                return Response(response_data, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_401_UNAUTHORIZED)


import requests
from django.http import JsonResponse   


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import urllib.parse

class BookSearchAPI(APIView):
    def get(self, request, query):
        client_id = "71GX1MGulezdAHHJXWQk"
        client_secret = "IJlwpjxdQk"
        encText = urllib.parse.quote(query)  # query 값을 책 이름으로 사용
        url = "https://openapi.naver.com/v1/search/book?query=" + encText + "&display=100"
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            items = result.get('items')
            return Response(items, status=status.HTTP_200_OK)
        
        return Response({}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, query):
        # POST 요청을 처리하고 데이터를 저장하는 로직을 여기에 추가합니다.
        # 네이버 도서 API에서 책 정보를 얻어와 UserBook 모델에 저장하는 예시를 들 수 있습니다.
        user_id = request.data.get('user_id')  # 사용자의 user_id 값을 가져옴
        user = CustomUser.objects.get(user_id=user_id)
        client_id = "71GX1MGulezdAHHJXWQk"
        client_secret = "IJlwpjxdQk"
        encText = urllib.parse.quote(query)  # query 값을 책 이름으로 사용
        url = "https://openapi.naver.com/v1/search/book?query=" + encText
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            result = response.json()
            items = result.get('items')

            # 사용자가 선택한 책 상태
            selected_state = request.data.get('state', UserBook.TO_READ)
            
            # 얻은 책 정보를 UserBook 모델에 저장
            for book_data in items:
                user = CustomUser.objects.get(user_id=request.user.user_id)  # 예시로 현재 로그인한 사용자를 가져옴
                UserBook.create_from_api(user, book_data)
                
            return Response(items, status=status.HTTP_200_OK)
        
        return Response({}, status=status.HTTP_400_BAD_REQUEST)


import urllib.parse
import requests
from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import UserBook

def save_user_book(request, user_id, isbn_str):
    isbn = int(isbn_str)  # 문자열로 받은 ISBN을 정수로 변환
    user_book = get_user_book_from_isbn(user_id, isbn)
    
    if user_book is None:
        # 해당 isbn으로 검색하여 UserBook 생성하는 코드
        book_info = get_book_info_from_isbn(isbn)
        if book_info is not None:
            user = get_object_or_404(CustomUser, id=user_id)
            user_book = UserBook(
                user=user,
                title=book_info['title'],
                author=book_info['author'],
                pubdate=book_info['pubdate'],
                isbn=isbn,
                publisher=book_info['publisher'],
                image=book_info['image'],
                state=UserBook.TO_READ
            )
            user_book.save()
            return Response({'message': 'UserBook saved successfully'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'message': 'Book information not found'}, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response({'message': 'UserBook already exists'}, status=status.HTTP_400_BAD_REQUEST)

def get_user_book_from_isbn(user_id, isbn):
    try:
        return UserBook.objects.get(user_id=user_id, isbn=isbn)
    except UserBook.DoesNotExist:
        return None

def get_book_info_from_isbn(isbn):
    client_id = "71GX1MGulezdAHHJXWQk"
    client_secret = "IJlwpjxdQk"
    encText = urllib.parse.quote(isbn)  # ISBN 값을 사용
    url = "https://openapi.naver.com/v1/search/book?query=" + encText
    headers = {
        "X-Naver-Client-Id": client_id,
        "X-Naver-Client-Secret": client_secret
    }
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        result = response.json()
        items = result.get('items')
        if items:
            # 여기서 items 중에서 필요한 정보를 추출하여 딕셔너리로 반환하면 됩니다.
            # 예시: {'title': 'Book Title', 'author': 'Author Name', ...}
            # 실제 API 응답 형식에 따라 결과를 가공해야 합니다.
            book_info = {
                'title': items[0].get('title'),
                'author': items[0].get('author'),
                'pubdate': items[0].get('pubdate'),
                'publisher': items[0].get('publisher'),
                'image': items[0].get('image'),
            }
            return book_info
    return None


class UserBookList(APIView):
    def get(self, request, user_id, state=None):
        if state is None:
            user_books = UserBook.objects.filter(user__user_id=user_id)
        else:
            user_books = UserBook.objects.filter(user__user_id=user_id, state=state)
        serialized_books = UserBookSerializer(user_books, many=True).data
        return Response(serialized_books, status=status.HTTP_200_OK)
    
    def post(selt, request, user_id, isbn):
        client_id = "71GX1MGulezdAHHJXWQk"
        client_secret = "IJlwpjxdQk"
        encText = urllib.parse.quote(isbn)  # ISBN 값을 사용
        url = "https://openapi.naver.com/v1/search/book?query=" + encText
        headers = {
            "X-Naver-Client-Id": client_id,
            "X-Naver-Client-Secret": client_secret
        }
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            result = response.json()
            items = result.get('items')
            if items:
                book_info = {
                    'title' : items[0].get('title'),
                    'author' : items[0].get('author'),
                    'pubdate' : items[0].get('pubdate'),
                    'isbn' : items[0].get('isbn'),
                    'publisher' : items[0].get('publisher'),
                    'image' : items[0].get('image'),
                }
        
        user_book = UserBook(
            user = user_id,
            title = book_info['title'],
            author=book_info['author'],
            pubdate=book_info['pubdate'],
            isbn=isbn,
            publisher=book_info['publisher'],
            image=book_info['image'],
            state=UserBook.TO_READ
        )
        user_book.save()