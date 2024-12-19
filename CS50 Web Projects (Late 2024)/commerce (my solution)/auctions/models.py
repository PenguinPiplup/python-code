from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator

categories={
    "NA": "No Category Listed",
    "Fashion": "Fashion",
    "Bags": "Bags",
    "Toys": "Toys",
    "Cameras": "Cameras",
    "Electronics": "Electronics",
    "Home": "Home",
    "Food & Drinks": "Food & Drinks",
    "Books": "Books",
    "Stationery": "Stationery",
    "Services": "Services"
}

class User(AbstractUser):
    pass

class Listing(models.Model):
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listed_items")
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=700)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.00)])
    imageurl = models.URLField(blank=True)
    category = models.CharField(choices=categories, max_length=50)
    current_bidder = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="leading_bids")
    current_bid = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    auction_closed = models.BooleanField(default=False)
    watchlist_members = models.ManyToManyField(User, blank=True, related_name="watchlisted_listings")

    #title = models.CharField(label="Title (Maximum of 120 characters)", max_length=120)
    #description = models.CharField(label="Description (Maximum of 700 characters)", max_length=700)
    #starting_bid = models.DecimalField(label="Starting Bid", decimal_places=2)
    #imageurl = models.URLField(label="Image URL", blank=True)
    #category = models.ChoiceField()

    def __str__(self):
        return f"{self.id}: {self.title} sold by {self.seller}"

class Bid(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="placed_bids")
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    datetime = models.DateTimeField(auto_now_add=False)

class Comment(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comments")
    commenter = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_by_user")
    comment = models.CharField(max_length=250)
    datetime = models.DateTimeField(auto_now_add=False)