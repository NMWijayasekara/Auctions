from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.exceptions import ObjectDoesNotExist
from .models import User, Auction, Bid, Comment, Watchlist
from django.db.models import Max
from django.utils.datastructures import MultiValueDictKeyError


def index(request):
    auctions = Auction.objects.all()
    return render(request, "auctions/index.html", {
        "auctions": auctions,
    })

def active_listings(request):
    auctions = Auction.objects.filter(active=True)
    bid = Bid.objects.all()
    return render(request, "auctions/index.html", {
        "auctions": auctions
    })

def new(request):
    user = request.user
    if user.is_authenticated:
        if request.POST:
            user = request.user
            name = request.POST['name']
            image_url = request.POST['image_url']
            description = request.POST['description']
            catelog = request.POST['catelog']
            bid = request.POST['bid']
            user = User.objects.get(username=user.username)
            a = Auction(title=name, description=description,
                    catelog=catelog, owner=user, image=image_url, bid=bid)
            a.save()
            return HttpResponseRedirect(reverse("index"))
    catelogs = [catelog[1] for catelog in Auction.catelogs]
    return render(request, "auctions/new.html", {
        "catelogs": catelogs
    })


def auction(request, title):
    user = request.user
    if user.is_authenticated:
        # auction function gobal variables
        auction = Auction.objects.get(title=title)
        user = request.user
        user = User.objects.get(username=user.username)
        bid = not(None)
        try:
            bid_earlier = Bid.objects.filter(auction=auction).latest()
        except Bid.DoesNotExist:
            bid = None
        bid_count = Bid.objects.filter(auction=auction).count()
        # bid on auction
        if request.POST:
            try:
                bid_new = int(request.POST['bid'])
                if bid_new <= auction.bid:
                    bid = Bid.objects.filter(auction=auction).first()
                    return render(request, "auctions/auction.html", {
                        "auction": auction,
                        "bid": bid,
                        "bid_count": bid_count,
                        "message": "Your bid must be greater than the earlier bid"
                    })
                elif bid != None:
                    if bid_new <= bid_earlier.bid:
                        bid = Bid.objects.filter(auction=auction).first()
                        return render(request, "auctions/auction.html", {
                            "auction": auction,
                            "bid": bid,
                            "bid_count": bid_count,
                            "message": "Your bid must be greater than the earlier bid"
                        })
                    else:
                        b = Bid.objects.create(
                            user=user, auction=auction, bid=bid_new)
                        b.save()
                else:
                    b = Bid.objects.create(user=user, auction=auction, bid=bid_new)
                    b.save()
            except MultiValueDictKeyError:
                bid_new = None
            # comment on auction
            try:
                comment = request.POST["comment"]
                c = Comment(user=user, auction=auction, comment=comment)
                c.save()
            except MultiValueDictKeyError:
                comment = None

    # view auction
    auction = Auction.objects.get(title=title)
    try:
        bid = Bid.objects.filter(auction=auction).latest()
    except Bid.DoesNotExist:
        bid = None
    comments = Comment.objects.filter(auction=auction)
    bid_count = Bid.objects.filter(auction=auction).count()
    if user.is_authenticated:
        try:
            watchlist = Watchlist.objects.get(user=user, auction=auction)
        except Watchlist.DoesNotExist:
            watchlist = None
    else:
        watchlist = None
    return render(request, "auctions/auction.html", {
        "auction": auction,
        "bid": bid,
        "bid_count": bid_count,
        "comments": comments,
        "watchlist": watchlist,
        "user": user
    })

def close_auction(request, title):
    auction = Auction.objects.get(title=title)
    auction.active = False
    auction.save()
    try:
        bid = Bid.objects.filter(auction=auction).latest()
        auction.winner = f"{bid.user}"
        auction.save()
    except Bid.DoesNotExist:
        bid = None

    print(f" The winner is {auction.winner}")
    return HttpResponseRedirect(reverse("active_listings"))

def watchlist(request, title):
    user = request.user
    if user.is_authenticated:
        auction = Auction.objects.get(title=title)
        user = User.objects.get(username=user.username)
        try:
            watchlist =  Watchlist.objects.get(user=user, auction=auction)
        except Watchlist.DoesNotExist:
            watchlist = None
    
        if watchlist == None:
            watchlist = Watchlist(user=user, auction=auction)
            watchlist.save()
        else:     
            watchlist.delete()

    return HttpResponseRedirect(reverse('auction', args=[title]))

def my_watchlists(request):
    user = request.user
    if user.is_authenticated:
        user = User.objects.get(username=user.username)
        watchlists = Watchlist.objects.filter(user=user)
        return render(request, "auctions/mywatchlists.html", {
            "watchlists": watchlists
        })

def my_auctions(request):
    user = request.user
    if user.is_authenticated:
        user = User.objects.get(username=user.username)
        auctions = Auction.objects.filter(owner=user)
        return render(request, "auctions/myauctions.html", {
            "auctions": auctions
        })

def catelogs(request):
    catelogs = [catelog[1] for catelog in Auction.catelogs]
    return render(request, "auctions/catelog.html", {
        "catelogs": catelogs
    })

def view_catelog(request, catelog):
    auctions = Auction.objects.filter(catelog=catelog)
    return render(request, "auctions/index.html", {
        "auctions": auctions,
        "catelog": catelog
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")
