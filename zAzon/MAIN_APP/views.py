from django.shortcuts import render
from .models import *
from django.http import *
from .forms import RegStep1, RegStep2, NewThread, NewPost
from django.contrib.auth.models import User


def main_page(request):
    user_count = User.objects.count()
    post_count = Post.objects.count()
    thread_count = Thread.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request, "main_page.html", {"user_count": user_count, "post_count": post_count, "thread_count": thread_count, "num_visits": num_visits})


def board(request, board):
    if board in ('Magic', 'TVs', 'Raccoons', 'Chill'):
        threads = Thread.objects.filter(board=board)
        thread_list = []
        for thread in threads:
            thread_list.append({'date': thread.thread_date,
                                "thread": thread.thread,
                                "login": thread.login,
                                "count": Post.objects.filter(thread=thread).count(),
                                "id": thread.id})

        if request.method == 'POST':
            thread = request.POST.get('thread')
            op_post = request.POST.get('op_post')
            login = User.objects.get(username=request.user.username)
            new_thread = Thread.objects.create(thread=thread, board=board, login=login, op_post=op_post)
            red = str(board) + '/Thread=' + str(new_thread.id)
            return HttpResponsePermanentRedirect(red)
        else:
            return render(request, "board.html", {"threads": thread_list, "board": board, "NewThread": NewThread})
    else:
        return HttpResponseBadRequest("<h2>Bad Request</h2>")


def thread(request, board, thread_id):
    if board in ('Magic', 'TVs', 'Raccoons', 'Chill'):
        posts = Post.objects.filter(thread_id=thread_id)
        thread = Thread.objects.get(id=thread_id)
        post_list = []
        for post in posts:
            post_list.append({"date": post.date,
                              "post": post.post,
                              "login": post.login,
                              "status": User_det.objects.get(username=User.objects.get(username=post.login)).status})

        if request.method == 'POST':
            post = request.POST.get('post')
            login = User.objects.get(username=request.user.username)
            new_post = Post.objects.create(thread=thread, post=post, login=login)
            post = Post.objects.filter(thread_id=thread_id)
            return render(request, "thread.html", {"board": board, "thread": thread, "posts": post_list, "NewPost": NewPost})
        else:
            return render(request, "thread.html", {"board": board, "thread": thread, "posts": post_list, "NewPost": NewPost})
    else:
        return HttpResponseBadRequest("<h2>Bad Request</h2>")


def user_page(request, user):
    ri = User.objects.get(username=user)
    details = User_det.objects.get(username_id=ri.id)
    posts = Post.objects.filter(login=user).reverse()
    activity = []
    for post in posts:
        thread = Thread.objects.get(thread=post.thread)
        activity.append({"date": post.date,
                         "post": post.post,
                         "ref": '/' + str(thread.board) + '/Thread=' + str(thread.id),
                         "thread": thread.thread})
    if request.user.is_authenticated and str(request.user.username) == str(details.username):
        user_check = True
    else:
        user_check = False
    return render(request, "user_page.html", {"details": details, "user_check": user_check, "posts": activity})


def edit(request):
    username = request.user.username
    ri = User.objects.get(username=username)
    if request.method == 'POST':
        name1 = request.POST.get("name")
        info1 = request.POST.get("info")
        status1 = request.POST.get("status")
        User_det.objects.filter(username=ri).update(name=name1, info=info1, status=status1)
        return user_page(request, username)
    else:
        initial = User_det.objects.get(username_id=ri.id)
        form = RegStep2(initial={'info': initial.info, 'status': initial.status, 'name': initial.name})
    return render(request, "registration/edit.html", {"form": form, "username": username})


def register(request):
    if request.method == 'POST':
        if request.POST.get('password1') == request.POST.get('password2'):
            username1 = request.POST.get("username")
            password1 = request.POST.get("password1")
            email1 = request.POST.get("email")
            new_user = User(username=username1, email=email1)
            new_user.set_password(password1)
            new_user.save()
            name1 = request.POST.get("name")
            info1 = request.POST.get("info")
            status1 = request.POST.get("status")
            new_user_det = User_det(username=new_user, name=name1, info=info1, status=status1)
            new_user_det.save()
            return render(request, "registration/registration_complete.html")
        else:
            return render(request, "registration/registration.html", {"step1": RegStep1, "step2": RegStep2, "error": "Passwords do not match!"})
    else:
        return render(request, "registration/registration.html", {"step1": RegStep1, "step2": RegStep2})



