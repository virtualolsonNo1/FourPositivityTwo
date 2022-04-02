from django.contrib import admin

# Register your models here.

from .models import Message
from .models import Profile
from .models import StoreItem

admin.site.register(Message)
admin.site.register(Profile)
admin.site.register(StoreItem)