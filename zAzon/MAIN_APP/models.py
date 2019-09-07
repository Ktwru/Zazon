from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User


class Board(models.Model):
    name = models.CharField(max_length=50)


class Thread(models.Model):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    description = models.TextField()
    date = models.DateTimeField(auto_now=True)
    pic = models.ImageField(null=True, blank=True, upload_to='threads')

    def __str__(self):
        return self.name


class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, 'posts')
    post = models.TextField()
    login = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now=True)
    pic = models.ImageField(null=True, blank=True, upload_to='posts', default=None)

    def __str__(self):
        return self.post


class MyUser(AbstractUser):
    name = models.CharField(max_length=100, null=True, blank=True, default='')
    info = models.TextField(null=True, blank=True)
    status = models.TextField(max_length=250, null=True, blank=True)
    pic = models.ImageField(upload_to='users', default=None)
    threads = models.ManyToManyField('Thread', 'users')

    def __str__(self):
        return str(self.name)
