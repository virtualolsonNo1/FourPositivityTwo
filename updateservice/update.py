from datetime import datetime
from django.utils import timezone
import pytz
from base.models import Profile
from django.core.mail import send_mail

# look up date=datetime.now() or testing function
def updateDailyPoints(now=datetime.now()):
    seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    # if it's within the minutes 0:00, set all users points to send to 100
    if seconds_since_midnight <= 60:
        profiles = Profile.objects.all()
        for profile in profiles:
            profile.pointsToSend = 100
            profile.save()

def notifyUsers():
    profiles = Profile.objects.all()
    # for every profile, if they haven't sent a message or gotten a notification in a day and have notifications on, send 
    # them an email saying such
    sent_message = False
    for profile in profiles:
        seconds_since_last_message = (datetime.now(profile.lastMessageSent.tzinfo) - profile.lastMessageSent).total_seconds()
        if (seconds_since_last_message >= 86400 and profile.notificationsOn):
            print("message sent")
            profile.lastMessageSent = datetime.now()
            profile.save()
            send_mail("We've missed you!!!", "You haven't sent a message in over a day", 'bigpapiprogramming@gmail.com', [str(profile.email)], fail_silently=False)
            print(profile.email)
            sent_message = True
    return sent_message