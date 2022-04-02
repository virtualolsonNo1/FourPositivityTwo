from django.forms import ModelForm
from .models import Message, Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'body']


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class SettingsForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['email', 'privacyOn', 'notificationsOn', 'profilePic']