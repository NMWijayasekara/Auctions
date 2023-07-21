from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Auction(models.Model):
    catelogs = (
    ("Household", "Household"),
    ("Toys", "Toys"),
    ("Fashion", "Fashion"),
    ("Accessories", "Accessories"),
    ("Books", "Books"),
    ("Other", "Other")
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=300)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    bid = models.IntegerField()
    winner = models.CharField(max_length=100, blank=True)
    catelog = models.CharField(max_length=15, choices=catelogs, blank=True)
    image = models.URLField(blank=True)
    time_created = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

 
    def __str__(self):
        return f"{self.title} | {self.description} | {self.owner} | ${self.bid} | {self.catelog} | Created: {self.time_created}"


class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_user")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="bids_auction")
    bid = models.IntegerField()
    time_bid = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"{self.user} has bid ${self.bid} for {self.auction.title} | Bidded on : {self.time_bid}"
    class Meta:
        get_latest_by = "time_bid"
        
class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_user")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="watchlist_auction")

    def __str__(self):
        return f"{self.user} is watching {self.auction.title}"

class Comment(models.Model):
    comment = models.CharField(max_length=300)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_user")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, related_name="comments_auction")
    time_commented = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} has commented to {self.auction.title}"
