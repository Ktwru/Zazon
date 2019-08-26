from django.contrib import admin
from .models import Thread, Post, User_det


admin.site.register(User_det)
admin.site.register(Post)
admin.site.register(Thread)
