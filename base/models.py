from django.db import models

from django.contrib.auth.models import User


class Review(models.Model):
    # Review Content
    title = models.CharField(max_length=200)
    summary = models.CharField(max_length=200)
    body = models.TextField()
    # TODO: add images to show.
    # Foreign Keys
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.title

    def short_content(self):
        return f'{self.body[0:200]}' + '...' if len(self.body) > 200 else self.body


class Comment(models.Model):
    # Comment Content
    body = models.TextField(blank=False)
    # Foreign Keys
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE)
    # Timestamps
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return f'{self.body[0:32]}'
