from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    def __str__(self):
        return f"{self.username}"

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.name}"

class AuctionListing(models.Model):
    title = models.CharField(max_length=16)
    description = models.CharField(max_length=16)
    startBid = models.CharField(max_length=16)
    url = models.CharField(max_length=268)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    watchers = models.ManyToManyField(User, blank=True, related_name="watchlist")
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="category")

# class Bid():
#     pass

# class Comment():
#     pass
