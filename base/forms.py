from django.forms import ModelForm
from django.contrib.auth.models import User

from .models import Review


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = '__all__'
        exclude = ['author']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
