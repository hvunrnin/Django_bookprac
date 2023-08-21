from rest_framework import serializers
from .models import CustomUser, Book, UserBook

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields=('user_name','user_email','user_id','user_password','user_date')

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields=('id', 'title','author','pubdate','isbn','publisher', 'image')

class UserBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBook
        fields=('id', 'user', 'title','author','pubdate','isbn','publisher', 'image', 'state')