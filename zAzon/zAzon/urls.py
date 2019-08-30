"""zAzon URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from MAIN_APP import views
from django.urls import re_path
from django.urls import include
from django.conf.urls.static import static

urlpatterns = [
    path('registration', views.register),
    re_path(r'users/.+/edit', views.edit),
    re_path(r'users/(?P<user>.+)/activity', views.user_activity),
    re_path(r'users/(?P<user>.+)', views.user_page),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin', admin.site.urls),
    re_path(r'(?P<board>\w+)/Thread=(?P<thread_id>.+)', views.thread),
    re_path(r'(?P<board>\w+)', views.board),
    re_path('', views.main_page),
] #+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
