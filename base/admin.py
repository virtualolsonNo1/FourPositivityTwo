from django.contrib import admin

# Register your models here.

from .models import Message
from .models import Profile
from .models import StoreItem
from .models import PurchaseItem
from .models import PublicProfile

admin.site.register(Message)
admin.site.register(Profile)
admin.site.register(StoreItem)
admin.site.register(PurchaseItem)
admin.site.register(PublicProfile)