from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class AuctionListing(models.Model):
    # Categories - choices
    MOTORS = "MOT"
    FASHINON = "FAS"
    ELECTRONICS = "ELE"
    COLLECTIBLES_ARTS = "ART"
    HOME_GARDES = "HGA"
    SPORTING_GOODS = "SPO"
    TOYS = "TOY"
    BUSSINES_INDUSTRIAL = "BUS"
    MUSIC = "MUS"

    CATEGORY = [
        (MOTORS, "Motors"),
        (FASHINON, "Fashion"),
        (ELECTRONICS, "Electronics"),
        (COLLECTIBLES_ARTS, "Collectibles & Art"),
        (HOME_GARDES, "Home & Garden"),
        (SPORTING_GOODS, "Sporting Goods"),
        (TOYS, "Toys"),
        (BUSSINES_INDUSTRIAL, "Business & Industrial"),
        (MUSIC, "Music"),
    ]

    title = models.CharField(max_length=16)
    description = models.CharField(max_length=16)
    startBid = models.CharField(max_length=16)
    url = models.CharField(max_length=268)
    seller = models.ForeignKey(User, on_delete=models.CASCADE)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    category = models.CharField(max_length=3, choices=CATEGORY, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    closed = models.BooleanField(default=False)
    currentPrice = models.DecimalField(max_digits=11, decimal_places=2, default=0.0)

class Bid(models.Model):
    auction = models.ForeignKey(AuctionListing, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=11, decimal_places=2)

    def __str__(self):
        return f"{self.user} bid {self.price} $ on {self.auction}"

# class Comment():
#     pass
