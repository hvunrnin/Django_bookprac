from django.urls import path, include
from . import views
from rest_framework import routers


router = routers.DefaultRouter(trailing_slash=False)
router.register('CustomUser', views.CustomUserview)
router.register('Book', views.Bookview)
router.register('UserBook', views.UserBookview)

urlpatterns = [
    path('', include(router.urls)),
    #path('api-auth/', include('rest_framework.urls')),
    path('hello_drf/', views.hello_drf),
    path('home', views.main, name='main'),
    path('createForm/', views.createForm, name='createForm'),
    path('createForm/createUser/', views.createUser, name='createUser'),
    path('loginForm/', views.loginForm, name="loginForm"),
    path('userpage/', views.custom_login, name='custom_login'), 
    path('logout/', views.custom_logout, name='custom_logout'), 
    path('add_user_book/', views.add_user_book, name='add_user_book'),
    path('delete_user_book/', views.delete_user_book, name='delete_user_book'),
    path('mybooks/', views.mybooks, name='mybooks'), 
    path('api_book_search', views.api_book_search1, name='api_book_search'),
    path('test/', views.test),
    #path('api/saveUserbook/<int:userid>/<int:isbn>', views.save_user_book, name='save_user_book'),


    # 회원가입
    path('api/user/', views.User.as_view(), name='user-list'),
    path('api/user/<str:user_id>/', views.User.as_view(), name='user-detail'),

    # 로그인
    path('login/<str:user_id>/', views.UserLogin.as_view(), name='user-detail'),
    path('login/', views.UserLogin.as_view(), name='user-login'),

    # 제목으로 OPEN API에서 책 찾기
    path('openapi/<str:query>/', views.BookSearchAPI.as_view(), name='api_book_search'),

    # 사용자 책
    path('userbook/<str:user_id>/', views.UserBookList.as_view(), name='userbook'),
    path('userbook/<str:user_id>/<str:state>/', views.UserBookList.as_view(), name='userbook-detail'),

      path('userbooksave/<str:user_id>/<isbn_str>/', views.save_user_book, name='save_user_book'),
]