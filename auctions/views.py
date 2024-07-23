from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User, AuctionListing, Category


def index(request):
    return render(request, "auctions/index.html", {
        "auctions": AuctionListing.objects.all()
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
    
def create_listing(request):
    if request.method == "POST":
        # try:
            category = request.POST["category"]
            category = Category.objects.filter(name=category).first()
            user = request.user
            description = request.POST["description"]
            title = request.POST["title"]
            startBid = request.POST["starting_bid"]
            url = request.POST["url"]
            AuctionListing.objects.create(title=title, description=description, startBid=startBid, user=user, url=url, category=category)
            return render(request, 'auctions/create_listing.html', {
                "message": "Listing created successfuly!"
            })
        # except Exception:
        #     return render(request, 'auctions/create_listing.html', {
        #         "message": "Error on creating listing!"
        #     })
    else:
        return render(request, "auctions/create_listing.html")
    
def listings(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    return render(request, "auctions/listings.html", {
        "listing": listing
    })

def watchlist(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    if request.method == "POST":
        listing.usersWatching.add(request.user)
        listing.save()
        return HttpResponseRedirect(reverse("listings", args=(listing.id,)))
    return render(request, "auctions/listings.html", {
            "listing": listing
        })