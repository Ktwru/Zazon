from django.shortcuts import render
from .models import *

def main_page(request):
    user_count = User.objects.count()
    post_count = Post.objects.count()
    thread_count = Thread.objects.count()
    return render(request, "main_page.html", {"user_count":user_count, "post_count":post_count, "thread_count": thread_count})


def TVs(request):
    return render(request, "boards/TVs.html")


def raccoons(request):
    return render(request, "boards/raccoons.html")


def magic(request):
    return render(request, "boards/magic.html")


def chill(request):
    return render(request, "boards/chill.html")