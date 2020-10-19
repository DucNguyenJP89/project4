
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    
    #API route
    path("posts/compose", views.compose, name="compose"),
    path("posts/<int:post_id>", views.post_info, name="post_info"),
    path("posts/<str:postview>", views.posts, name="posts"),
]
