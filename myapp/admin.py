from django.contrib import admin
from myapp.models import CustomUser, Book, UserBook

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Book)
admin.site.register(UserBook)