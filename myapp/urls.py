from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter(trailing_slash=False)
router.register('CustomUser', views.CustomUserview)
router.register('Book', views.Bookview)
router.register('UserBook', views.UserBookview)

urlpatterns = [
    path('', include(router.urls)),
    path('home', views.main, name='main'),
    path('createForm/', views.createForm, name='createForm'),
    path('createForm/createUser/', views.createUser, name='createUser'),
    path('loginForm/', views.loginForm, name="loginForm"),
    path('userpage/', views.custom_login, name='custom_login'), 
    path('logout/', views.custom_logout, name='custom_logout'), 
    path('test/', views.test)
]