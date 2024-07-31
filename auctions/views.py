from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django import forms

from .models import User, AuctionListing, Bid


class BidForm(forms.ModelForm):
    # Creates form for Bid model.
    class Meta:
        model = Bid
        fields = ["price"]
        labels = {
            "price": _("")
        }
        widgets = {
            "price": forms.NumberInput(attrs={
                "placeholder": "Bid",
                "min": 0.01,
                "max": 1000000000,
                "class": "form-control"
            })
        }

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
            user = request.user
            description = request.POST["description"]
            title = request.POST["title"]
            startBid = request.POST["starting_bid"]
            url = request.POST["url"]
            AuctionListing.objects.create(title=title, description=description, startBid=startBid, seller=user, url=url, category=category)
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
    auction = AuctionListing.objects.get(pk=listing_id)
    print(auction.watchers.all())

    # Get info about bids
    bid_amount = Bid.objects.filter(auction=listing_id).count()
    highest_bid = Bid.objects.filter(auction=listing_id).order_by('-price').first()

    return render(request, "auctions/listings.html", {
        "auction": auction,
        "bid_form": BidForm(),
        "bid_amount": bid_amount
    })

def addRemoveWatchlist(request, listing_id):
    listing = AuctionListing.objects.get(pk=listing_id)
    if request.method == "POST":
        if(listing.watchers.contains(request.user)):
            listing.watchers.remove(request.user)
        else:
            listing.watchers.add(request.user)
        listing.save()
        print(listing.watchers.contains(request.user))
        return HttpResponseRedirect(reverse("listings", args=(listing.id,)))
    return render(request, "auctions/listings.html", {
            "listing": listing
        })

def watchlist(request):
    watchlist = request.user.watchlist.all()
    return render(request, "auctions/index.html", {
            "auctions": watchlist
        })

@login_required(login_url="auctions:login")
def bid(request):
    # Bid view: only POST methos allowed, handles bidding logic.
    if request.method == "POST":
        form = BidForm(request.POST)
        if form.is_valid():
            price = float(form.cleaned_data["price"])
            auction_id = request.POST.get("auction_id")

            auction = AuctionListing.objects.get(pk=auction_id)
            user = User.objects.get(id=request.user.id)

            if auction.seller == user:
                return render(request, "auctions/error_handling.html", {
                    "code": 400,
                    "message": "Seller cannot bid"
                })
            
            highest_bid = Bid.objects.filter(auction=auction).order_by('-price').first()
            if highest_bid is None or price > highest_bid.price:
                # Add new bid to db
                new_bid = Bid(auction=auction, user=user, price=price)
                new_bid.save()

                # Update current highest price
                auction.currentPrice = price
                auction.save()

                return HttpResponseRedirect(f"listings/{auction_id}")
            else:
                return render(request, "auctions/error_handling.html", {
                    "code": 400,
                    "message": "your bid is too small"
                })
        else:
            return render(request, "auctions/error_handling.html", {
                "code": 400,
                "message": "Form is invalid"
            })
    return render(request, "auctions/error_handling.html", {
        "code": 405,
        "message": "Method Not Allowed"
    })