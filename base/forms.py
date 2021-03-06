from tkinter.tix import Form
from django.forms import EmailField, EmailInput, ModelForm
from matplotlib import widgets
from .models import Message, Profile, PublicProfile, PurchaseItem
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

        # widgets = {
        #     'email': EmailInput(attrs={
        #         'style' : 'font-size: 40px'
        #     })
        # }

class PurchaseForm(ModelForm):
    class Meta:
        model = PurchaseItem
        fields = ['item']
class ProfileForm(ModelForm):
    def __init__(self,*args,**kwargs):
        super (ProfileForm,self ).__init__(*args,**kwargs)
        self.fields['profile'].queryset = Profile.objects.filter(privacyOn=False)
    class Meta:
        model = PublicProfile
        fields = ['profile']