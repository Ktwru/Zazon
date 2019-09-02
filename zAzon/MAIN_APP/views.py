from django.shortcuts import render
from .models import *
from django.http import *
from .forms import RegStep1, RegStep2, NewThread, NewPost
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate


def main_page(request):
    user_count = User.objects.count()
    post_count = Post.objects.count()
    thread_count = Thread.objects.count()

    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    return render(request, "main_page.html",
                  {"user_count": user_count, "post_count": post_count, "thread_count": thread_count,
                   "num_visits": num_visits})


def board(request, board):
    if board == 'Magic': desc = 'Board about magic!'
    if board == 'TVs': desc = 'Board about TVs.'
    if board == 'Raccoons': desc = 'Board about raccoons!'
    if board == 'Chill': desc = 'Board for chill...'

    if board in ('Magic', 'TVs', 'Raccoons', 'Chill'):
        threads = Thread.objects.filter(board=board)
        thread_list = []
        for thread in threads:
            thread_list.append({'date': thread.date,
                                "thread": thread.thread,
                                "login": thread.login,
                                "count": Post.objects.filter(thread=thread).count(),
                                "id": thread.id,
                                "pic": thread.pic,
                                "op_post": thread.op_post,
                                "op_pic": User_det.objects.get(username=User.objects.get(username=thread.login)).pic})

        if request.method == 'POST':
            form = NewThread(request.POST, request.FILES)
            file = request.FILES['pic']

            thread = request.POST.get('thread')
            op_post = request.POST.get('op_post')
            login = User.objects.get(username=request.user.username)
            new_thread = Thread.objects.create(thread=thread, board=board, login=login, op_post=op_post, pic=file)
            red = str(board) + '/Thread=' + str(new_thread.id)
            return HttpResponsePermanentRedirect(red)
        else:
            form = NewThread()
            return render(request, "board.html",
                          {"threads": thread_list, "board": board, "NewThread": form, "desc": desc})
    else:
        return HttpResponseBadRequest("<h2>Bad Request</h2>")


def thread(request, board, thread_id):
    if board == 'Magic': desc = 'Board about magic!'
    if board == 'TVs': desc = 'Board about TVs.'
    if board == 'Raccoons': desc = 'Board about raccoons!'
    if board == 'Chill': desc = 'Board for chill...'

    if board in ('Magic', 'TVs', 'Raccoons', 'Chill') and Thread.objects.filter(id=thread_id).exists():
        posts = Post.objects.filter(thread_id=thread_id)
        post_list = []
        for post in posts:
            details = User_det.objects.get(username=User.objects.get(username=post.login))
            post_list.append({"date": post.date,
                              "post": post.post,
                              "login": post.login,
                              "pic": post.pic,
                              "status": details.status,
                              "user_pic": details.pic})
        thread = Thread.objects.get(id=thread_id)
        threadone = {"date": thread.date, "pic": thread.pic, "thread": thread.thread,
                    "login": thread.login, "op_post": thread.op_post, "op_pic": User_det.objects.get(username=thread.login).pic}
        if request.method == 'POST':
            post = request.POST.get('post')
            if 'pic' in request.FILES: file = request.FILES['pic', False]
            else: file = None
            login = User.objects.get(username=request.user.username)
            new_post = Post.objects.create(thread=thread, post=post, login=login, pic=file)

            return HttpResponsePermanentRedirect(request.path)
        else:
            return render(request, "thread.html",
                          {"board": board, "thread": threadone, "posts": post_list, "NewPost": NewPost, "desc": desc})
    else:
        return HttpResponseBadRequest("<h2>Bad Request</h2>")


def user_page(request, user):
    ri = User.objects.get(username=user)
    details = User_det.objects.get(username_id=ri.id)

    posts = Post.objects.filter(login=user).reverse()
    threads = Thread.objects.filter(login=ri.id)
    activity = []
    for j in posts:
        in_thread = Thread.objects.get(id=j.thread_id)
        activity.append({"date": j.date,
                         "content": user + ':' + j.post,
                         "thread": 'in ' + str(j.thread),
                         "ref": '/' + str(in_thread.board) + '/Thread=' + str(in_thread.id)})
    for j in threads: activity.append({"date": j.date,
                                       "content": user + " created a thread:",
                                       "thread": str(j.thread),
                                       "ref": '/' + str(j.board) + '/Thread=' + str(j.id)})
    act = sorted(activity, key=lambda k: k['date'], reverse=True)

    if request.user.is_authenticated and str(request.user.username) == str(details.username):
        user_check = True
    else:
        user_check = False
    return render(request, "user_page.html", {"details": details, "user_check": user_check, "activity": act[:5]})


def edit(request):
    username = request.user.username
    ri = User.objects.get(username=username)
    if request.method == 'POST':
        name1 = request.POST.get("name")
        info1 = request.POST.get("info")
        status1 = request.POST.get("status")
        user_det = User_det.objects.filter(username=ri)
        user_det.update(name=name1, info=info1, status=status1)
        if 'pic' in request.FILES:
            file = request.FILES['pic']
            user_det.update_or_create(defaults={"pic": file})
        return HttpResponsePermanentRedirect('/users/' + str(username))
    else:
        initial = User_det.objects.get(username_id=ri.id)
        form = RegStep2(initial={'info': initial.info, 'status': initial.status, 'name': initial.name, 'pic': initial.pic})
    return render(request, "registration/edit.html", {"form": form, "username": username})


def user_activity(request, user):
    ri = User.objects.get(username=user)
    posts = Post.objects.filter(login=user).reverse()
    threads = Thread.objects.filter(login=ri.id)
    activity = []
    for j in posts:
        in_thread = Thread.objects.get(id=j.thread_id)
        activity.append({"date": j.date,
                         "content": user + ':' + j.post,
                         "thread": 'in ' + str(j.thread),
                         "ref": '/' + str(in_thread.board) + '/Thread=' + str(in_thread.id)})
    for j in threads: activity.append({"date": j.date,
                                       "content": user + " created a thread:",
                                       "thread": str(j.thread),
                                       "ref": '/' + str(j.board) + '/Thread=' + str(j.id)})
    act = sorted(activity, key=lambda k: k['date'], reverse=True)
    return render(request, 'user_activity.html', {'activity': act, 'user': user})


def register(request):
    if request.method == 'POST':
        if request.POST.get('password1') == request.POST.get('password2'):
            username1 = request.POST.get("username")
            password1 = request.POST.get("password1")
            email1 = request.POST.get("email")
            name1 = request.POST.get("name")
            info1 = request.POST.get("info")
            status1 = request.POST.get("status")
            if User.objects.filter(username=username1).exists():
                return render(request, "registration/registration.html",
                              {"step1": RegStep1, "step2": RegStep2, "error": "User " + username1 + ' already exists!'})
            if 'pic' in request.FILES: file = request.FILES['pic']
            else: file = None
            new_user = User(username=username1, email=email1)
            new_user.set_password(password1)
            new_user.save()
            new_user_det = User_det.objects.create(username=new_user, name=name1, info=info1, status=status1, pic=file)
            user = authenticate(username=username1, password=password1)
            login(request, user)
            return render(request, "registration/registration_complete.html")
        else:
            return render(request, "registration/registration.html",
                          {"step1": RegStep1, "step2": RegStep2, "error": "Passwords do not match!"})
    else:
        return render(request, "registration/registration.html", {"step1": RegStep1, "step2": RegStep2})
