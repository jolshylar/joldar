from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Custom Fields
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    avatar = models.ImageField(upload_to="avatars/", default="avatar.svg")
    # Custom Configuration
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


class Review(models.Model):
    # Review Content
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=200)
    body = models.TextField()
    image = models.ImageField(upload_to="uploads/", null=True)
    # Foreign Keys
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return self.title

    def short_content(self):
        return f"{self.body[0:100]}..." if len(self.body) > 100 else self.body


class Comment(models.Model):
    # Comment Content
    body = models.TextField(blank=False)
    # Foreign Keys
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated", "-created"]

    def __str__(self):
        return f"{self.body[0:32]}"
