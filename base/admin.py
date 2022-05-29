from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from base.models import Comment, Review, User

admin.site.register(User, UserAdmin)
admin.site.register(Review)
admin.site.register(Comment)
