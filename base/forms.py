from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from base.models import Review


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ["name", "username", "email", "password1", "password2"]


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = "__all__"
        exclude = ["author"]


class UserForm(ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["avatar", "name", "username", "email"]
