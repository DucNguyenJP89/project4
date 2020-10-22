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

@csrf_exempt
@login_required
def post_info(request, post_id):
    
    user = User.objects.get(username=request.user)
    # Query for requested email
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    # Return post content
    if request.method == "GET":
        return JsonResponse(post.serialize())

    # Update post content or favorite
    if request.method == "PUT":
        data = json.loads(request.body)
        if data.get("content") is not None:
            if post.poster != user:
                return JsonResponse({"error": "You have no permission to edit this post"}, status=403)
            elif post.poster == request.user:
                post.content = data["content"]
        if data.get("liked") is not None:
            post_info = post.serialize()
            if user.username in post_info["liked"]:
                post.liked.remove(user)
            elif user.username not in post_info["liked"]:
                post.liked.add(user)
        post.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({"error": "GET or PUT request required"}, status=400)

@csrf_exempt
def user_info(request, username):
    
    # Query for following user
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return JsonResponse({"error": "User not found."}, status=404)
    
    # Query for request user info
    try:
        user_info = UserInfo.objects.get(user=user)
    except UserInfo.DoesNotExist:
        user_info = {"following": [], "followers": []}

    # Get user info: follow info and all posts
    if request.method == "GET":
        # Get all posts of user
        posts = Post.objects.filter(poster=user)
        posts = posts.order_by("-timestamp").all()
        
        return JsonResponse({"info": user_info.serialize(), "posts": [post.serialize() for post in posts]}, safe=False)
    
    if request.method == "PUT":
        
        # Get request user info
        request_user = User.objects.get(username=request.user)
        request_user_info = UserInfo.objects.get(user=request_user)

        # user cannot follow himself
        if request.user == username:
            return JsonResponse({"error": "You cannot follow yourself"}, status=403)
        
        data = json.loads(request.body)
        if data.get("follow") is not None:
            user_follow = user_info.serialize()
            if request.user in user_follow["followers"]:
                user_info.followers.remove(request_user)
                request_user_info.following.remove(user)
            elif request.user not in user_follow["followers"]:
                user_info.followers.add(request_user)
                request_user_info.following.add(user)
        
        user_info.save()
        request_user_info.save()
        return HttpResponse(status=204)
    
    else:
        return JsonResponse({"error": "GET or PUT request required"}, status=400)


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
        # Add user info data as well
        user = User.objects.get(username=username)
        user_info = UserInfo(user=user)
        user_info.save()

        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
