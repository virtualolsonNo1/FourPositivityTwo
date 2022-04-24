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
            print(user.email)
            send_mail("We've missed you!!!", "You haven't sent a message in over a day", 'bigpapiprogramming@gmail.com', [str(user.email)], fail_silently=False)
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
    sender.save()
    reciever.save()
    return True
@login_required(login_url='login')
def createMessage(request):
    form = MessageForm()
    validReceivers  = User.objects.filter(~Q(username=request.user.username))
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
    context = {'form': form,'validReceivers':validReceivers}
    return render(request, 'base/message_form.html', context)

def purchaseItem(item,profile):
    if profile.pointsReceived < item.cost:
        error = "Error not enough points!"
        print("Error not enough points!")
        return error
    profile.pointsReceived = profile.pointsReceived- item.cost
    profile.save()
    item.timesPurchased = item.timesPurchased + 1
    item.save()
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
            if purchased.item in itemRecentBuyers:
                buyers = itemRecentBuyers[purchased.item]
                if purchased.user.username not in buyers:
                    buyers.append(purchased.user.username)
                    itemRecentBuyers = buyers
            else:
                itemRecentBuyers[purchased.item] = [purchased.user.username]
            print(itemRecentBuyers[purchased.item])
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
    context = {'storeItems': storeItems,'form':form, 'userPoints':userPoints,'userInventory':userItems,'itemRecentBuyers':itemRecentBuyers}
    return render(request, 'base/store.html', context)

@login_required(login_url='login')
def profile(request):
    form = ProfileForm()
    user = request.user
    inventory = PurchaseItem.objects.filter(user=request.user.id)
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
    context = {'user': user,'inventory':inventory,'form':form}
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

def distributePoints():
    profiles = Profile.objects.all()
    for profile in profiles:
        profile.pointsToSend = 100
        profile.save()
