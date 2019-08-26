from django.shortcuts import render
from .models import *
from django.http import HttpResponse

def main_page(request):
    user_count = User.objects.count()
    post_count = Post.objects.count()
    thread_count = Thread.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request, "main_page.html", {"user_count":user_count, "post_count":post_count, "thread_count": thread_count, "num_visits": num_visits})


def board(request, board):
    threads = Thread.objects.filter(board=board)
    cnt = [Post.objects.filter(thread=thread).count() for thread in threads]
    return render(request, "board.html", {"threads": threads, "cnt": cnt, "board": board})


def thread(request, board, thread_id):
    post = Post.objects.filter(thread_id=thread_id)
    thread = Thread.objects.get(id=thread_id)
    return render(request, "thread.html", {"board": board, "thread": thread, "posts": post})


def user_page(request, user):
    ri = User.objects.get(username=user)
    details = User_det.objects.get(username_id=ri.id)
    return render(request, "user_page.html", {"details": details})


