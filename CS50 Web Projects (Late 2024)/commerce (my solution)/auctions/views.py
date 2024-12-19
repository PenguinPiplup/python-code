from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
import datetime

from .models import User, Listing, Bid, Comment
from .models import categories as category_list

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "description", "starting_bid", "imageurl", "category"]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]


def index(request):
    Active_Listings = Listing.objects.filter(auction_closed = False)
    return render(request, "auctions/index.html", {
        "Active_Listings": Active_Listings
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
    
def view_item(request, id):
    def view_item_get(request, id):
        id = int(id)
        listing = Listing.objects.get(pk=id)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "CommentForm": CommentForm()
        })

    if request.method == "POST":
        bid = round(float(request.POST.get("bid")), 2)
        listing = Listing.objects.get(pk=int(id))
        if listing.auction_closed == True:
            return HttpResponse("Forbidden: Auction has been closed")
        
        min_bid = round(max(float(listing.starting_bid), float(listing.current_bid) + 0.01), 2)
        if bid >= min_bid:
            NewBid = Bid(listing=listing, bidder=request.user, bid_amount=bid, datetime=datetime.datetime.now())
            NewBid.save()
            listing.current_bidder = request.user
            listing.current_bid = bid
            listing.save()
            return view_item_get(request, id)
        else:
            return render(request, "auctions/bid_error.html", {
            "id": id,
            "min_bid": f"{min_bid:.2f}"
        })

    else:
        return view_item_get(request, id)
        

# Create a new listing
@login_required
def create(request):
    if request.method == "POST":
        form = ListingForm(request.POST)
        
        if form.is_valid():
            seller = request.user
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            starting_bid = form.cleaned_data["starting_bid"]
            imageurl = form.cleaned_data["imageurl"]
            category = form.cleaned_data["category"]
            listed_item = Listing(seller=seller, title=title, description=description, starting_bid=starting_bid, imageurl=imageurl, category=category)
            listed_item.save()
            return HttpResponseRedirect(reverse("index"))

    else:   
        return render(request, "auctions/create.html",{
            "form": ListingForm()
        })

@login_required
def watchlist(request):
    return render(request, "auctions/watchlist.html", {
        "user_watchlist": request.user.watchlisted_listings.all()
    })

@login_required
def add_watchlist(request, id):
    id_num = int(id)
    listing = Listing.objects.get(pk=id_num)
    current_user = request.user
    current_user.watchlisted_listings.add(listing)
    return HttpResponseRedirect(reverse("view_item", args=[id]))

@login_required
def remove_watchlist(request, id):
    id_num = int(id)
    listing = Listing.objects.get(pk=id_num)
    current_user = request.user
    current_user.watchlisted_listings.remove(listing)
    return HttpResponseRedirect(reverse("view_item", args=[id]))

def categories(request):
    return render(request, "auctions/categories.html", {
        "category_list": category_list
    })

def view_category(request, category):
    category_items = Listing.objects.filter(category=category, auction_closed=False)
    return render(request, "auctions/view_category.html", {
        "category": category,
        "category_items": category_items
    })

@login_required
def close_auction(request, id):
    listing = Listing.objects.get(pk=int(id))
    if request.user != listing.seller:
        return HttpResponse(f"Forbidden: User is not {listing.seller}")
    
    listing.auction_closed = True
    listing.save()

    Active_Listings = Listing.objects.filter(auction_closed = False)
    return render(request, "auctions/auction_closed_success.html", {
        "Active_Listings": Active_Listings
    })

@login_required
def comment(request, id):
    if request.method == "POST":
        listing = Listing.objects.get(pk=int(id))
        comment = request.POST.get("comment")
        NewComment = Comment(listing=listing, commenter=request.user, comment=comment, datetime=datetime.datetime.now())
        NewComment.save()
        return HttpResponseRedirect(reverse("view_item", args=[id]))
    else:
        return HttpResponse("Forbidden: Comment form not submitted")