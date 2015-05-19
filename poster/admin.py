from django.contrib import admin
from poster.models import *
from django.contrib.auth.models import User
# Register your models here.
admin.site.register(Post)
admin.site.unregister(User)
admin.site.register(User)
admin.site.register(user_post)
admin.site.register(Like)