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

urlpatterns = [
    re_path(r'^TVs', views.TVs),
    re_path(r'^Raccoons', views.raccoons),
    re_path(r'^Magic', views.magic),
    re_path(r'^Chill', views.chill),
    re_path('', views.main_page),
    path('admin', admin.site.urls),
]
