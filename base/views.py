from django.conf import Settings
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, SettingsForm
from .forms import MessageForm
from .models import Message
from .models import Profile
# 10 Points: 😊🤩👏🥰❤️🌈🌹🌻☀️🙌🌟
# 20 Points:✨🏅💖🍨🍕🎈🐶🐱🐸💫
# 50 Points: 💎👑💛
# 100 Points: 💯
EMOJIS = {"😊":10,"👏" : 10, "🤩" : 10,"❤️": 10, "🌈" : 10, "🙌":10,"🌟":10,"💫":20, 
"🥰":10,"🏅":20,"🎈":20,"💖":20,"👑":50,"🐶":20,"💛" : 50,"✨":20,
"🐱":20,"🐸":20,"🌹":20,"🌻":10,"☀️":10,"🍨":20,"🍕":20,"💎":50,"💯":100}

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = user.email.lower()
            user.save()
            Profile.objects.create(
                user=user,
                email = user.email
            )
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    if(request.user.username is not ''):
        user = User.objects.get(username=request.user.username)
    else:
        context = {}
        return render(request, 'base/home.html', context)

    profiles = Profile.objects.all()
    for profile in profiles:
        if profile.user == request.user:
            print(profile.pointsToSend)



    q = request.GET.get('q') if request.GET.get('q') != None else ''
    messages_to = user.receiver.all()
    messages_to = messages_to.filter( 
        Q(sender__username__icontains=q)
        )
    message_count = messages_to.count()

    unique_senders = user.receiver.all()
    senders = []
    for message in unique_senders:
        if message.sender not in senders:
            senders.append(message.sender)

    context = {'message_count': message_count, 'messages': messages_to, 'senders': senders}
    return render(request, 'base/home.html', context)

def getPoints(message):
    print(message)
    chars = list(message)
    pointTotal = 0
    for char in chars:
        if char in EMOJIS.keys():
            pointTotal += EMOJIS[char]
            print(char + " : pointTotal " + str(pointTotal))
    return pointTotal

def message(request, pk):
    message = Message.objects.get(id=pk)
    context = {'message': message}
    return render(request, 'base/message.html', context)
def updatePoints(senderName,recieverName,pointTotal):
    sender = Profile.objects.get(user=senderName.id)
    reciever = Profile.objects.get(user=recieverName.id)

    # check sender has enough points
    if reciever.pointsToSend < pointTotal:
        print("Error not enough sender points!")
        return False

    # decrement sender points
    print("Sender " + senderName.username + " spent " + str(pointTotal) + " sender points")
    print("Sender points before " +  str(sender.pointsToSend))
    sender.pointsToSend = sender.pointsToSend - pointTotal
    print("Sender points after " +  str(sender.pointsToSend))
    # increment reciever points 
    print("Reciever " + recieverName.username + " recieved " + str(pointTotal) + " points")
    print("Reciever points before " +  str(reciever.pointsReceived))
    reciever.pointsReceived = reciever.pointsReceived + pointTotal
    print("Reciever points after " +  str(reciever.pointsReceived))
    return True
@login_required(login_url='login')
def createMessage(request):
    form = MessageForm()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.sender = request.user
            # get points for emojis in the message
            pointTotal = getPoints(obj.body)
            obj.pointTotal = pointTotal

            # decrement sender points and increment reciever points
            success = updatePoints(obj.sender,obj.receiver, pointTotal)          
            if success:
                obj.save()
                return redirect('home')
            else:
                # print error message
                return 
    context = {'form': form}
    return render(request, 'base/message_form.html', context)

@login_required(login_url='login')
def store(request):
    context = {'storeItems': "buy some pizza"}
    return render(request, 'base/store.html', context)

@login_required(login_url='login')
def profile(request):
    user = request.user
    context = {'user': user}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def leaderboard(request):
    profiles = Profile.objects.all()
    profiles = profiles[:10]
    context = {'topSenders': profiles}
    return render(request, 'base/leaderboard.html', context)

@login_required(login_url='login')
def settings(request):
    user = request.user
    profiles = Profile.objects.all()
    for profile in profiles:
        if profile.user == user:
            profile = Profile.objects.get(user=user)
    form = SettingsForm(instance=profile)
    # IF USER ADMIN PANEL USED, request won't be post so doesn't work??????
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            user.email = profile.email
            user.save(update_fields=['email'])
            return redirect('home')
    context = {'form': form}
    return render(request, 'base/settings.html', context)
