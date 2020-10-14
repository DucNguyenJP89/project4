import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.db import IntegrityError
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.urls import reverse

from .models import User, UserInfo, Post


def index(request):
    return render(request, "network/index.html")

@csrf_exempt
@login_required
def compose(request):

    # Composing a new email must be via POST
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    # Get content of the post
    data = json.loads(request.body)
    content = data.get("content")
    user = User.objects.get(username=request.user)
    # Create post
    post = Post(
        poster=user,
        content=content
    )

    post.save()
    return JsonResponse({"message": "Post created successfully."}, status=201)

def posts(request, postview):
    
    # Filter posts returned base on post view
    if postview == "all":
        posts = Post.objects.all() 
    elif postview == "following":
        # Get user from request user
        user = User.objects.get(username=request.user)
        
        # Get following info based on user
        following=UserInfo.objects.filter(user=user).values("following")
        
        # Get all posts of following
        posts = Post.objects.filter(poster__in=following)
    else:
        return JsonResponse({"Error": "Invalid view"}, status=400)
    
    # Return posts in reverse chronological order
    posts = posts.order_by("-timestamp").all()
    return JsonResponse([post.serialize() for post in posts], safe=False)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
