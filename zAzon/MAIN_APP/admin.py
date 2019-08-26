from django.contrib import admin
from .models import User_info, Thread, Post


admin.site.register(User_info)
admin.site.register(Post)
admin.site.register(Thread)