from django.contrib import admin

# Register your models here.

from .models import Message
from .models import Profile

admin.site.register(Message)
admin.site.register(Profile)