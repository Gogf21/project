from django.contrib import admin
from .models import User


from .models import UserPost

admin.site.register(UserPost)
admin.site.register(User)