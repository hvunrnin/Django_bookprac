from django.shortcuts import render
from rest_framework import viewsets
from .models import CustomUser, Book, UserBook
from .serializers import CustomUserSerializer, BookSerializer, UserBookSerializer
from rest_framework.generics import ListAPIView
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

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

def custom_login(request):
    if request.method == 'POST':
        userid = request.POST.get('userid')
        password = request.POST.get('password')
        #lists = Book.objects.all()
        #book = {'lists':lists} 

        try:
            user = CustomUser.objects.get(user_id=userid)
        except CustomUser.DoesNotExist:
            user = None

        if user and user.user_password == password:
            login(request, user)
            user_info={'user_id': user.user_id}
            #lists = UserBook.objects.filter(user=user)
            lists = UserBook.objects.all()  # Book 객체 목록을 가져옴
            data = {'lists': lists, 'user_info': user_info}
            #data = {'book':book, 'user_info':user_info}
            #return redirect('myBooks', user_id=user.user_id)
            #return HttpResponse(f'{user.user_id}')
            return render(request, 'mybooks.html', data)
        else:
            return HttpResponseRedirect(reverse('main'))  # 로그인 실패 시 메인 페이지로 이동
    return HttpResponse("d")

def custom_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main'))

def test(request):
    lists = Book.objects.all()
    data = {'lists':lists} 
    return render(request, 'mybooks.html', data)