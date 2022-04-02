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
    pointTotal = models.IntegerField

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.body[0:50]

class Profile(models.Model):
    profilePic = models.ImageField(null=True, blank=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    email = models.EmailField(null=True, blank=True)
    notificationsOn = models.BooleanField(default=True)
    privacyOn = models.BooleanField(default=False)
    pointsToSend = models.IntegerField(default=100)
    pointsReceived = models.IntegerField(default=0)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pointsReceived']

    def __str__(self):
        return str(self.user)