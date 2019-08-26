from django.contrib import admin
from .models import Thread, Post


admin.site.register(Post)
admin.site.register(Thread)