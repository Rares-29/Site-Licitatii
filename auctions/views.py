from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import User, Item, Bid, Comment,Category,Watchlist

def index(request):
    items = Item.objects.all()
    return render(request, "auctions/index.html",{
        'items': items,
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
                "message": "User sau/si parola gresite."
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
        location = request.POST["location"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        #daca parola nu se potriveste
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Parola trebuie sa se potriveasca."
            })

        # Incearca sa creeze un usser nou.
        try:
            user = User.objects.create_user(username, email, password, location = location)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "user-ul deja exista."
            })
        watchlist = Watchlist(user = username)
        watchlist.save()  
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def product(request, product_id):
    bid = Bid.objects.get(item = product_id)
    item = Item.objects.get(id = product_id)
    comments = item.comments.all()
    if request.method == "POST" and 'y_offer' in request.POST:
        offer = int(request.POST["y_offer"])
        Nume = request.POST["Nume"]
        Numar = request.POST["Numar"]
        print(offer)
        print(Nume)
        print(Numar)
        print('da')
        if  offer > bid.offer:
            bid.offer = offer
            bid.peoples = bid.peoples + 1
            bid.Number = Numar
            bid.Name = Nume
            bid.bidder = request.user.get_username()
            bid.save()
            return render(request, 'auctions/product.html',{
                'item':item,
                'bid':bid,
                'comments':comments
            })
        else:
            return render(request, 'auctions/product.html',{
                'item':item,
                'bid':bid,
                'comments': comments,
                'error': "Please insert a higher value!"
            })
    elif request.method == "POST" and 'button' in request.POST:
        item.winner = bid.bidder
        item.save()
    elif request.method == "POST" and 'comment' in request.POST:
        comment = request.POST['comment']
        user = request.user.get_username()
        comm = Comment(user_com = user, comment = comment, product_id = item)
        comm.save()
    elif request.method == "POST" and 'watchlist' in request.POST:
        watchlist = Watchlist.objects.get(user = request.user.get_username())
        if Watchlist.objects.filter(user=request.user, product=item.id).exists():
            watchlist.product.remove(item.id)
        else:
            watchlist.product.add(item.id)
    return render(request, 'auctions/product.html',{
        'item':item,
        'bid':bid,
        'comments': comments
    })

def category_general(request):
    category = Category.objects.all()
    return render(request, 'auctions/category_general.html',{
        'categories': category
    })

def category(request, category):
    items = Item.objects.filter(category = category)
    return render(request, 'auctions/categories.html',{
        'items': items
    })

def watchlist(request):
    if request.user.is_authenticated:
        watchlist = Watchlist.objects.get(user = request.user.get_username())
        product = watchlist.product.all()
        return render(request, 'auctions/watchlist.html',{
        'product': product})
    else:
        return HttpResponseRedirect(reverse("register"))
    

def create_listing(request):
    categories = Category.objects.all()
    if request.method == "POST":
        new_item = Item()
        new_item.name = request.POST["title"]
        new_item.description = request.POST["description"]
        new_item.price = request.POST["price"]
        new_item.category = Category.objects.get(id = int(request.POST["category"]))
        new_item.seller = request.user.get_username()
        if len(request.FILES) != 0:
            new_item.Image = request.FILES["image"]
        new_item.save()
        bid = Bid(offer = new_item.price, item = new_item, peoples = 0)
        bid.save()
    return render(request, 'auctions/create_listing.html',{
        'categories':categories
    })