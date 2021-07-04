import json
from datetime import datetime

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.utils.http import urlencode
from django.utils.timezone import make_aware
from webpush import send_user_notification

from auction.models import *
from django.core.mail import send_mail

def index(request):
    webpush_settings = getattr(settings, 'WEBPUSH_SETTINGS', {})
    vapid_key = webpush_settings.get('VAPID_PUBLIC_KEY')
    user = request.user
    return render(request, 'auction/index.html', {user: user, 'vapid_key': vapid_key})

def validateAuction(request):
    if request.POST['phrase'] != '':
        auction = Auction.objects.filter(_passphrase=request.POST['phrase'])
        if len(auction) > 0:
            response = redirect('/auction/auction/' + request.POST['phrase'])
            response.set_cookie('auction', request.POST['phrase'])
            if request.user.is_authenticated:
                request.user.addAuction(auction[0])
                request.user.changeCurrentAuction(auction[0])
            return response
        return redirect('/auction?error=invalid')

def auction(request, phrase):
    auction = get_object_or_404(Auction, _passphrase=phrase)
    items = auction.getItems()
    if request.GET:
        if "cols" in request.GET:
            request.user.changeColumns(int(request.GET["cols"]))
        if "search" in request.GET:
            items = items.filter(_name__contains=request.GET["search"])
        if "category" in request.GET:
            if (request.GET["category"] == "favorites"):
                items = request.user.getCurrentFavorites()
            elif (request.GET['category'] == 'live'):
                items = auction.getLiveItems()
            else:
                items = items.filter(_category=request.GET["category"])
    return render(request, 'auction/auction.html', {'auction': auction, 'items': items, 'cats': Item.Categories})


def item(request, phrase, id):
    auction = get_object_or_404(Auction, _passphrase=phrase)
    item = get_object_or_404(Item, pk=id)
    if request.GET:
        if "fav" in request.GET:
            if request.GET["fav"] == "add":
                request.user.addFavorite(item);
            else:
                request.user.removeFavorite(item);
    return render(request, 'auction/item.html', {'auction': auction, 'item': item})

def loginPage(request):
    return render(request, 'auction/login.html', {})

def forgotPassword(request):
    return render(request, 'auction/forgotPassword.html', {})

def resetPassword(request):
    return render(request, 'auction/resetPassword.html', {})

def profile(request, id):
    bidder = get_object_or_404(Bidder, pk=id)

@login_required(login_url='../login')
def profile(request):
    bidder = get_object_or_404(Bidder, pk=request.user.id)
    return render(request, 'auction/profile.html', {'bidder': bidder})

@login_required(login_url='../login')
def myAuctions(request):
    bidder = get_object_or_404(Bidder, pk=request.user.id)
    return render(request, 'auction/myAuctions.html', {'bidder': bidder})

def signup(request):
    return render(request, 'auction/signup.html', {})

def createBidder(request):
    # Create a bidder
    bidder = Bidder()
    bidder.changeName("Test Bidder")
    bidder.changeEmail("test@bidder.com")
    bidder.changePassword("supersecure")
    bidder.changeAuction(auction)
    bidder.save()

def processLogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        #Add the user to the current auction
        if 'auction' in request.COOKIES and request.COOKIES['auction'] != '':
            auction = Auction.objects.filter(_passphrase=request.COOKIES['auction'])
            if len(auction) > 0:
                user.addAuction(auction[0])
                user.changeCurrentAuction(auction[0])

        if request.POST['next'] != '':
            return redirect(request.POST['next'])
        return redirect('/auction')
    else:
        return redirect('/auction/login?error=invalid&next=' + request.POST['next'])

def processLogout(request):
    logout(request)
    if request.GET['next'] != '':
        return redirect(request.GET['next'])
    return redirect('/auction/login')

def processSignup(request):
    first_name = request.POST['fname']
    last_name = request.POST['lname']
    email = request.POST['email']
    password = request.POST['password']
    password2 = request.POST['password2']

    #Check if user already exists
    userCount = Bidder.objects.filter(email=email).count()
    if userCount > 0:
        return redirect('/auction/signup?error=duplicate&next=' + request.POST['next'])
    ## If the password doesn't match
    if password != password2:
        return redirect('/auction/signup?error=badpass&next=' + request.POST['next'])

    bidder = Bidder(first_name=first_name, last_name=last_name, email=email)
    ## If the password doesn't meet our requirements
    if not bidder.changePassword(password):
        return redirect('/auction/signup?error=badpass&next=' + request.POST['next'])
    login(request, bidder)
    # Add the user to the current auction
    if 'auction' in request.COOKIES and request.COOKIES['auction'] != '':
        auction = Auction.objects.filter(_passphrase=request.COOKIES['auction'])
        if len(auction) > 0:
            bidder.addAuction(auction[0])
            bidder.changeCurrentAuction(auction[0])
    if request.POST['next'] != '':
        return redirect(request.POST['next'])
    return redirect('/auction')

def processForgotPassword(request):
    email = request.POST['email']

    # Check if user exists
    user = Bidder.objects.filter(email=email)
    if len(user) < 1:
        return redirect('/auction/login/forgotPassword?error=nouser')

    hash = user[0].generateResetHash()
    user[0].save()
    messageText = 'You have requested that your email be reset. Please navigate to http://localhost:8000/auction/login/resetPassword?h=' + hash + ' to reset your password. '
    messageHtml = 'You have requested that your email be reset. Please navigate to <a href="http://localhost:8000/auction/login/resetPassword?h=' + hash + '">http://localhost:8000/auction/login/resetPassword?h=' + hash + '</a> to reset your password.'

    send_mail(
        'Password Reset',
        messageText,
        'Alpha Auction <no-reply@blazerunner44.me>',
        [email],
        fail_silently=False,
        html_message=messageHtml
    )
    return redirect('/auction/login/forgotPassword?error=success')

def resetPasswordProcess(request):
    hash = request.POST['hash']
    password = request.POST['password']

    # Check if user already exists
    user = Bidder.objects.filter(_resetHash=hash)
    if len(user) < 1:
        return redirect('/auction/login/resetPassword?h='+hash+'&error=nouser')

    if user[0].changePassword(password):
        return redirect('/auction/login?error=passwordreset')
    return redirect('/auction/login/resetPassword?h=' + hash + '&error=minreq')

@login_required(login_url='../../../../../auction/login')
def processBid(request, phrase, id):
    amount = request.POST['amount']
    bidder = request.user
    item = get_object_or_404(Item, id=id)
    # Get current winner before bid is processed
    prevWinner = item.getWinner()

    bid = Bid(_bidPrice = amount, _bidder = bidder, _item = item)
    try:
        bid.save()
        if prevWinner != request.user and prevWinner is not None:
            payload = {'head': "You've been outbid!", 'url': "http://localhost:8000/auction/auction/" + str(item.getAuction().getPass()) + "/item/" + str(item.pk), 'body': "You've been outbid on " + item.getName() + ". Return to the auction to place a new bid!"}
            send_user_notification(prevWinner, payload, ttl=1000)

        return redirect(f'/auction/auction/{phrase}/item/{id}/')
    except Exception as e:
        print(e)
        return redirect(f'/auction/auction/{phrase}/item/{id}/?error=failure')

def processFavorite(request, phrase, id):
    item = get_object_or_404(Item, id=id)
    if request.GET["fav"] == "add":
        request.user.addFavorite(item)
    else:
        request.user.removeFavorite(item)
    return redirect(f'/auction/auction/{phrase}/item/{id}/')


def auctionEndPush(request):
    try:
        user = request.user;
        if user.is_superuser:
            userSent = []

            for item in Item.objects.all():
                winner = item.getWinner()
                if winner is not None and winner not in userSent:
                    userSent.append(winner)
                    payload = {'head': "You've won items!", 'url': "http://localhost:8000/auction/myAuctions/", 'body': 'The auction has ended and you\'ve won items! Check out your profile for details.'}
                    send_user_notification(user=winner, payload=payload, ttl=1000)
        else:
            return JsonResponse(status=401, data={"message": "Access denied"})
        return JsonResponse(status=200, data={"message": "Web push successful"})
    except TypeError:
        return JsonResponse(status=500, data={"message": "An error occurred"})
        

