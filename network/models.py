from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class UserInfo(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE, primary_key=True, related_name='user_info')
    followers = models.ManyToManyField("User", related_name="user_followers")
    following = models.ManyToManyField("User", related_name="user_following")

class Post(models.Model):
    poster = models.ForeignKey("User", on_delete=models.CASCADE, related_name='user_posting')
    content = models.TextField(blank=False)
    liked = models.ManyToManyField("User", blank=True, related_name='liked_users')
    unliked = models.ManyToManyField("User", blank=True, related_name='unliked_users')
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return {
            "id": self.id,
            "poster": self.poster.username,
            "content": self.content,
            "liked": [user.id for user in self.liked.all()],
            "unliked": [user.id for user in self.unliked.all()],
            "timestamp": self.timestamp.strftime("%b %-d %Y, %_I:%M %p")
        }
    
    def __str__(self):
        return f"Post {self.id} by {self.poster.username}."