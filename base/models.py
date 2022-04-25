from django.db import models

from django.contrib.auth.models import User


class Review(models.Model):
    # Review Content
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=200)
    body = models.TextField()
    # TODO: may add images to show.
    # Foreign Keys
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Time
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title


class Comment(models.Model):
    # Comment Content
    body = models.TextField()
    # Foreign Keys
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    # Time
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return f'{self.body[0:32]} ...'
