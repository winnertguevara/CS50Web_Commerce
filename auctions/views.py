from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import *
from .models import *

def index(request):
    return render(request, "auctions/index.html")

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
            messages.add_message(request, messages.ERROR, 'Invalid username and/or password.')
            return render(request, "auctions/login.html")
    else:
        return render(request, "auctions/login.html")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"].lower()
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            messages.add_message(request, messages.ERROR, 'Passwords must match.')
            return render(request, "auctions/register.html")

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            messages.add_message(request, messages.ERROR, 'Username already taken.')
            return render(request, "auctions/register.html")
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create_listing(request):
        
    if request.method == "POST":
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            new_list = form.save(commit=False)
            new_list.listedBy = request.user
            new_list.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()
    return render(request, "auctions/create_listing.html", {"form": form })

def listing_page(request, listing_id):
    listing = Listing.objects.get(id = listing_id)
    bids_list = Bid.objects.filter(listing=listing.id)
    comments_list = Comment.objects.filter(listing=listing.id)
        
    if str(request.user) == str(listing.listedBy):
        flag = False
    else:
        flag = True
        
    if request.method == "POST":
        bid_form = BidForm()
        comment_form = CommentForm()
        
        if 'bid_save' in request.POST:
            bid_form = BidForm(request.POST)
            if bid_form.is_valid():
                new_bid = bid_form.save(commit=False)
                if new_bid.bid <= listing.price:
                    messages.add_message(request, messages.ERROR, 'Your bid must be greather than the current bid.')
                    bid_form = BidForm()
                else:
                    new_bid.listing = Listing.objects.get(id = request.POST["listing"])
                    new_bid.user = User.objects.get(id = request.POST["user"])
                    new_bid.save()
                    listing.price = new_bid.bid
                    listing.save()      
                    return HttpResponseRedirect(reverse("listing_page", args=[listing_id]))  
        elif 'comment_save' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                new_comment = comment_form.save(commit=False)
                new_comment.user = User.objects.get(id = request.POST["user"])
                new_comment.listing = Listing.objects.get(id = request.POST["listing"])
                new_comment.save()
                return HttpResponseRedirect(reverse("listing_page", args=[listing_id]))

    else:
        bid_form = BidForm()
        comment_form = CommentForm()
    
    return render(request, "auctions/listing_page.html", {"listing_id": listing_id,
                                                          "title": listing.title,
                                                          "price": listing.price,
                                                          "description": listing.description,
                                                          "category": listing.category,
                                                          "image": listing.image,
                                                          "listedBy": listing.listedBy,
                                                          "bids_list" : len(bids_list),
                                                          "comments_list": comments_list,
                                                          "bid_form": bid_form,
                                                          "comment_form": comment_form,
                                                          "flag": flag,
                                                          "winner": listing.winner,
                                                          "active": listing.active
                                                          }) 

@login_required(login_url='login')
def create_watchlist(request,listing_id):
    listing = Listing.objects.get(id = listing_id)
    user = User.objects.get(username = request.user)
    listing.watchlist.add(user)
    messages.add_message(request, messages.SUCCESS, 'Listing added to your watchlist.')
    return HttpResponseRedirect(reverse("listing_page", args=[listing_id]))

def remove_watchlist(request, listing_id):
    listing = Listing.objects.get(id = listing_id)
    user = User.objects.get(username = request.user)
    user.listing_set.remove(listing)
    messages.add_message(request, messages.SUCCESS, 'Listing removed from your watchlist.')
    return HttpResponseRedirect(reverse("view_watchlist"))
 
def view_watchlist(request):
    user = User.objects.get(username = request.user)    
    watchlist = Listing.objects.filter(watchlist = user.id)
    return render (request, "auctions/watchlist.html", {"watchlist": watchlist,
                                                        })

def categories_list(request):
    categories=[]
    listing_list = Listing.objects.all()
    for listing in listing_list:
        if listing.category in categories:
            pass
        else:
            categories.append(listing.category)
    return render(request, "auctions/categories.html",{"categories": categories})  

def category(request, category):
    if category == 'no_category':
        category_list = Listing.objects.filter(category = '')   
    else:
        category_list = Listing.objects.filter(category = category)
    return render (request, "auctions/category.html", {"category": category,
                                                       "category_list": category_list
                                                       })  

def close_listing(request, listing_id):
    listing = Listing.objects.get(id = listing_id)
    listing.active = False
    winner_bid = Bid.objects.filter(listing = listing_id, bid = listing.price)
    if len(winner_bid) > 0:
        listing.winner = winner_bid[0].user
    listing.save()
    messages.add_message(request, messages.SUCCESS, 'Your auction is already close.')
    return HttpResponseRedirect(reverse("index"))