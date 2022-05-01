from turtle import update
from django.conf import Settings
from django.dispatch import receiver
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CreateUserForm, SettingsForm, PurchaseForm
from .forms import MessageForm,ProfileForm
from .models import Message
from .models import Profile
from .models import StoreItem
from .models import PurchaseItem
from django.core.mail import send_mail
from django.core.files.storage import FileSystemStorage
# 10 Points: 😊🤩👏🥰❤️🌈🌹🌻☀️🙌🌟
# 20 Points:✨🏅💖🍨🍕🎈🐶🐱🐸💫
# 50 Points: 💎👑💛
# 100 Points: 💯
EMOJIS = {"😊":10,"👏" : 10, "🤩" : 10,"❤️": 10, "🌈" : 10, "🙌":10,"🌟":10,"💫":20, 
"🥰":10,"🏅":20,"🎈":20,"💖":20,"👑":50,"🐶":20,"💛" : 50,"✨":20,
"🐱":20,"🐸":20,"🌹":20,"🌻":10,"☀️":10,"🍨":20,"🍕":20,"💎":50,"💯":100}

def loginPage(request):
    # specify page
    page = 'login'

    # if user is already logged in, redirect to home
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        # if user exists, grab them, otherwise, send error that user does not exist
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)

        # if user exists and is authenticated, log them in and redirect them to the home page, otherwise, specify username or
        # password doesn't exist
        if user is not None:
            login(request, user)
            print(user.email)
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

    # if the request is a post, make sure the registrationform is valid, update the user email if it was changed, 
    # log the user in, and redirect them to the home page
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
        # otherwise, send error message that an error occurred during registration
        else:
            messages.error(request, 'An error occured during registration')

    return render(request, 'base/login_register.html', {'form': form})

def home(request):
    page = 'Home'

    # if username isn't blank, grab user object, otherwise, render home without user
    if(request.user.username is not ''):
        user = User.objects.get(username=request.user.username)
    else:
        context = {'page': page}
        return render(request, 'base/home.html', context)

    # grab messages send to user and send them to frontend to be displayed, allowing for them to be filtered by sender
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    messages_to = user.receiver.all()
    messages_to = messages_to.filter( 
        Q(sender__username__icontains=q)
        )
    message_count = messages_to.count()

    unique_senders = user.receiver.all()
    senders = []

    # create list of unique senders to be sent to the frontend so messages can be filtered by sender
    for message in unique_senders:
        if message.sender not in senders:
            senders.append(message.sender)

    context = {'message_count': message_count, 'messages_to': messages_to, 'senders': senders,'page': page}
    return render(request, 'base/home.html', context)

def getPoints(message):
    chars = list(message)
    pointTotal = 0

    # iterate through the message's body, totaling the number of points in the message based on emojis
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

    # check not sending to themselves
    if sender.id == reciever.id:
        error = "Error cannot send message to yourself"
        print(error)
        return error

    # check sender has enough points
    if reciever.pointsToSend < pointTotal:
        error = "Error not enough sender points!"
        print(error)
        return error

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
    sender.save()
    reciever.save()
    return ""
@login_required(login_url='login')
def createMessage(request):
    user = request.user
    page = 'Messages'
    form = MessageForm()
    validReceivers  = User.objects.filter(~Q(username=request.user.username))
    error = ""
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
            if success == "":
                obj.save()
                return redirect('home')
            else: 
                error = success
    context = {'form': form,'validReceivers':validReceivers,'error':error, 'page': page, 'user': user}
    return render(request, 'base/message_form.html', context)

def purchaseItem(item,profile):
    # if the user doesn't have enough points, send error saying that
    if profile.pointsReceived < item.cost:
        error = "Error not enough points!"
        print("Error not enough points!")
        return error
    profile.pointsReceived = profile.pointsReceived- item.cost
    profile.save()
    item.timesPurchased = item.timesPurchased + 1
    item.save()
    # otherwise, purchase item, updating the points and times purchased accordingly and sending confirmation message back
    message = "Successfully purchased " + str(item.name) + " for " + str(item.cost)
    print(message)
    return message
 
def addStoreItem(name, cost):
    newItem = StoreItem.objects.create(name=name,cost=20)
    newItem.save()
def editStoreImage(item,image):
    results = StoreItem.objects.filter(name=item)
    newItem = results[0]
    newItem.image = image
    newItem.save()
@login_required(login_url='login')
def store(request):
    page = "Store"
    form = PurchaseForm()
    storeItems = StoreItem.objects.all()
    userItems = PurchaseItem.objects.filter(user=request.user.id)

    # populate map of most recently purchased items and who has purchased 
    itemRecentBuyers = {}

    # purchased items in order of creation
    purchasedAll = PurchaseItem.objects.all()
    for purchased in purchasedAll:
        profile = Profile.objects.get(user=purchased.user.id)
        if profile.privacyOn is False:
            if purchased.item.id in itemRecentBuyers:
                buyers = itemRecentBuyers[purchased.item.id]
                if purchased.user.username not in buyers:
                    buyers.append(purchased.user.username)
                    itemRecentBuyers[purchased.item.id] = buyers
            else:
                itemRecentBuyers[purchased.item.id] = [purchased.user.username]
            print(itemRecentBuyers[purchased.item.id])
    print(str(itemRecentBuyers))
        
    currProf = Profile.objects.get(user=request.user.id)
    userPoints = currProf.pointsReceived
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            obj = form.save(commit = False)
            obj.user = request.user
            currProf = Profile.objects.get(user=request.user.id)
            # purchase
            success = PurchaseItem.purchase(obj.item,currProf)          
            if success:
                obj.save()
                return redirect('home')
            else:
                # print error message
                print("error purchase failed")
                return redirect('home')
        else:
            print("Error form is not valid")
    context = {'storeItems': storeItems,'form':form, 'userPoints':userPoints,'userItems':userItems,'itemRecentBuyers':itemRecentBuyers, 'page': page}
    return render(request, 'base/store.html', context)

@login_required(login_url='login')
def profile(request):
    page = 'Profile'
    form = ProfileForm()
    user = request.user
    inventory = PurchaseItem.objects.filter(user=request.user.id)

    # form to select another profile and call profile url with the other user's information
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            otherProf = form.save(commit=False)
            inventory = PurchaseItem.objects.filter(user=otherProf.profile.user.id)
            user = otherProf.profile.user
            print("Returning profile for " + str(user.username))
            context = {'user': user,'inventory':inventory,'form':form}
            return render(request, 'base/profile.html', context)
        else: 
            print("Form is not valid")
    print(str(inventory))
    context = {'user': user,'inventory':inventory,'form':form, 'page': page}
    return render(request, 'base/profile.html', context)

@login_required(login_url='login')
def leaderboard(request):
    page = 'Leaderboard'
    profiles = Profile.objects.all()
    profiles = profiles[:10]
    # after grabbing top 10 senders, send them to the front end to be displayed
    context = {'topSenders': profiles, 'page': page}
    return render(request, 'base/leaderboard.html', context)

@login_required(login_url='login')
def settings(request):
    page = 'Settings'
    user = request.user
    profile = Profile.objects.get(user=request.user.id)
    form = SettingsForm(instance=profile)
    # if user tries to update settings, update their settings according to values input and update the user email accordingly
    if request.method == 'POST':
        form = SettingsForm(request.POST, request.FILES, instance=profile)
        newPic = False
        if form.is_valid():
            form.save(commit=False)
            try:
                test = request.FILES['profilePic']
                newPic = True
            except:
                test = profile.profilePic
            profile.profilePic = test
            form.profilePic = test

            form.save()
            user.email = profile.email
            user.save(update_fields=['email'])
            if newPic is True:
                url = profile.profilePic.url
                profile.profilePic = url
            profile.save()
            return redirect('home')
    context = {'form': form, 'page': page}
    return render(request, 'base/settings.html', context)
