from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.conf import settings
from django.contrib import messages


from .models import User, Listings, Bids, Comment, Watch

from django.utils import timezone



def index(request):
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all()
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


@login_required
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

@login_required
def auct_list(request):
    if request.method == "POST":
        title = request.POST['title']
        description = request.POST['describe']
        starter = request.POST['starter']
        category = request.POST['category']
        owner = request.user
        image = False
        if 'image' in request.FILES:
            image = request.FILES['image']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT)
            fs.save(image.name, image)
            path = fs.url(image.name)
        # print(request.FILES)
        # print(path)
        # print(fs.location)
            new = Listings(title=title,description=description,start=starter,
                        category=category,image_url=path,owner=owner)
            new.save()
        else:
            new = Listings(title=title,description=description,start=starter,
                            category=category, owner=owner)
            new.save()
        # print(new.image_url)
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'auctions/create.html')

@login_required
def product(request, id):
    if request.method == "POST":
        amount = float(request.POST['bid']) 
        bidder = request.user
        item = Listings.objects.get(id=id)
        time = timezone.now()
        top = 0
        if Bids.objects.filter(item=Listings.objects.get(id=id)).order_by('-amount').first():
            top = Bids.objects.filter(item=Listings.objects.get(id=id)).order_by('-amount').first().amount
        if (amount >= item.start and
             (top is None or amount >= top)):

            new = Bids(amount=amount,bidder=bidder,item=item,time=time)
            new.save()
        else:
            messages.error(request, "Your bid is not sufficient.")
    
    item = Listings.objects.get(id=id)
    watched = False
    watch_count = 0
    if Watch.objects.filter(user=request.user,item=item).exists():
        watched = True
        watch_count = Watch.objects.filter(user=request.user).count() 
    winner = None
    o_item = Bids.objects.filter(item=Listings.objects.get(id=id)).order_by('-amount').first()
    if o_item:
        top = o_item.amount
        winner = o_item.bidder
    else:
        top = False
    return render(request, 'auctions/listing.html', {
        "listing": item,
        "top": top,
        "comments": Comment.objects.filter(item=item).order_by('-time'),
        "watched": watched,
        "winner": winner
    })

@login_required
def comment(request, id):
    if request.method == "POST":
        comment = request.POST["c_section"]
        commenter = request.user
        time = timezone.now()
        item = Listings.objects.get(id=id)
        new = Comment(comment=comment,commenter=commenter,time=time,item=item)
        new.save()
    return redirect('product', id=id)

@login_required
def watch(request):
    if request.method == "POST":
        id = request.POST['listing']
        item = Listings.objects.get(id=id)
        item.watched = "yes"
        item.save()
        new = Watch(user=request.user,item=item,time=timezone.now())
        new.save()
        watched = True
        top = Bids.objects.filter(item=Listings.objects.get(id=id)).order_by('-amount').first()
        if top:
            top = top.amount
        else:
            top = "No Bids Yet"
        return render(request,'auctions/listing.html', {
            "listing": item,
            "top": top,
            "comments": Comment.objects.filter(item=item).order_by('-time'),
            "watched": watched
        })
    print(Watch.objects.filter(user=request.user))
    return render(request, 'auctions/watch.html',{
        "listings": Watch.objects.filter(user=request.user)
    })

@login_required
def status(request):
    if request.method == "POST":
        item = Listings.objects.get(id=request.POST["close"])
        item.status = "closed"
        item.save()
    return render(request, "auctions/index.html", {
        "listings": Listings.objects.all()
        }) 
@login_required
def mine(request):
    my_listings = Listings.objects.filter(owner=request.user)
    return render(request, "auctions/mine.html", {
        "listings": my_listings
    })

@login_required
def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": Listings.objects.filter(status="open")
    })

@login_required
def categories_list(request, category):
    return render(request, "auctions/list.html", {
        "categories": Listings.objects.filter(category=category)
    })

@login_required
def remove_watch(request):
    if request.method == "POST":
        id = request.POST['listing']
        item = Listings.objects.get(id=id)
        item.watched = "no"
        item.save()
        item = Watch.objects.get(item=id)
        item.watched = "no"
        item.save()
    return render(request, 'auctions/watch.html',{
        "listings": Watch.objects.filter(user=request.user, watched="yes")
    })