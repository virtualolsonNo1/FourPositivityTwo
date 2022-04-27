from datetime import datetime
from django.utils import timezone
import pytz
from base.models import Profile
from django.core.mail import send_mail

def updateDailyPoints():
    now = datetime.now(timezone.utcoffset)
    seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    if seconds_since_midnight <= 60:
        profiles = Profile.objects.all()
        for profile in profiles:
            profile.pointsToSend = 100
            profile.save()

def notifyUsers():
    profiles = Profile.objects.all()
    for profile in profiles:
        seconds_since_last_message = (datetime.now(profile.lastMessageSent.tzinfo) - profile.lastMessageSent).total_seconds()
        if (seconds_since_last_message >= 86400):
            print("message sent")
            profile.lastMessageSent = datetime.now()
            profile.save()
            send_mail("We've missed you!!!", "You haven't sent a message in over a day", 'bigpapiprogramming@gmail.com', [str(profile.email)], fail_silently=False)
            print(profile.email)