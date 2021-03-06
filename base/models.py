from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
# Create your models here.


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    pointTotal = models.IntegerField()

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body[0:50]

class StoreItem(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    cost = models.IntegerField()
    timesPurchased = models.IntegerField(default=0)

    class Meta:
        ordering = ['-timesPurchased']

    def __str__(self):
        return self.name 
class Profile(models.Model):
    profilePic = models.ImageField(null=True, blank=True,default='/images/StoreAssets/SmileAssetRed.png')
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    notificationsOn = models.BooleanField(default=True)
    privacyOn = models.BooleanField(default=False)
    pointsToSend = models.IntegerField(default=100)
    pointsReceived = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    lastMessageSent = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pointsReceived']

    def __str__(self):
        return str(self.user)
        
class PublicProfile(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='+')  
class PurchaseItem(models.Model):
    item = models.ForeignKey(StoreItem, on_delete=models.CASCADE, related_name='+')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+')
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    def purchase(item,profile):
        if profile.pointsReceived < item.cost:
                error = "Error not enough points!"
                print("Error not enough points!")
                return False
        profile.pointsReceived = profile.pointsReceived- item.cost
        profile.save()
        item.timesPurchased = item.timesPurchased + 1
        item.save()
        message = "Successfully purchased " + str(item.name) + " for " + str(item.cost)
        print(message)
        return True 
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return str(self.item)