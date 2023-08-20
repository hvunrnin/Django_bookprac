from django.db import models

# Create your models here.
class CustomUser(models.Model):
    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=100)
    user_id = models.CharField(max_length=50)
    user_password = models.CharField(max_length=50)
    user_date = models.DateTimeField(auto_now_add=True)

    last_login = models.DateTimeField(auto_now=True)  

    def __str__(self):
        return self.user_id
    
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.PositiveIntegerField()
    genre = models.CharField(max_length=50, null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return self.title

class UserBook(models.Model):
    READ = 'read'
    READING = 'reading'
    TO_READ = 'to_read'
    
    STATE_CHOICES = [
        (READ, '읽은 책'),
        (READING, '읽고 있는 책'),
        (TO_READ, '읽고 싶은 책'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, default=None)  
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    publication_year = models.PositiveIntegerField()
    genre = models.CharField(max_length=50, null=True, blank=True)
    publisher = models.CharField(max_length=100, null=True, blank=True)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default=TO_READ)

    def __str__(self):
        return self.title
