from django.shortcuts import render
from .models import *

def main_page(request):
    user_count = User.objects.count()
    post_count = Post.objects.count()
    thread_count = Thread.objects.count()
    return render(request, "main_page.html", {"user_count":user_count, "post_count":post_count, "thread_count": thread_count})


def magic(request, board):
    threads = Thread.objects.filter(board=board)
    cnt = [Post.objects.filter(thread=thread).count() for thread in threads]
    return render(request, "board.html", {"threads": threads, "cnt": cnt, "board": board})