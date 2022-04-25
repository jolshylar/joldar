from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.conf import settings

from base.forms import ReviewForm, UserForm

from .models import Comment, Review


def home(request):
    all_reviews = Review.objects.all()
    context = {'all_reviews': all_reviews}
    return render(request, 'base/home.html', context)


def review(request, pk):
    review = Review.objects.get(id=pk)
    review_comments = review.comment_set.all()

    if request.method == 'POST':
        Comment.objects.create(
            body=request.POST.get('body'),
            author=request.user,
            review=review,
        )
        return redirect('review', pk=review.id)

    context = {
        'review': review,
        'review_messages': review_comments,
    }
    return render(request, 'base/review.html', context)


# ===== REVIEW CRUD =====

@login_required(login_url='login')
def create_review(request):
    form = ReviewForm()
    if request.method == 'POST':
        Review.objects.create(
            title=request.POST.get('title'),
            summary=request.POST.get('summary'),
            body=request.POST.get('body'),
            author=request.user,
        )
        return redirect('home')

    context = {'form': form}
    return render(request, 'base/review_form.html', context)


@login_required(login_url='login')
def update_review(request, pk):
    review = Review.objects.get(id=pk)
    form = ReviewForm(instance=review)

    if request.user != review.author:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        review.title = request.POST.get('title')
        review.summary = request.POST.get('summary')
        review.body = request.POST.get('body')
        review.save()
        return redirect('home')
    
    context = {'form': form, 'review': review}
    return render(request, 'base/review_form.html', context)


@login_required(login_url='login')
def delete_review(request, pk):
    review = Review.objects.get(id=pk)

    if request.user != review.author:
        return HttpResponse('You are not allowed here!')
    
    if request.method == 'POST':
        review.delete()
        return redirect('home')

    context = {'obj': review}
    return render(request, 'base/delete.html', context)


@login_required(login_url='login')
def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.author:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        comment.delete()
        # TODO: think whether to redirect to a parent comment or home
        return redirect('home')

    context = {'obj': comment}
    return render(request, 'base/delete.html', context)


# ===== ABOUT =====

def about(request):
    with open(settings.BASE_DIR / "static/markdown/about.md", "r") as f:
        context = {'markdown_content': f.read()}
    return render(request, 'base/about.html', context)


# ===== AUTHENTICATION =====

def register_page(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            # Login right after registration
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occurred during registration')
        
    context = {'form': form}
    return render(request, 'base/login_register.html', context)


def login_page(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password entered wrong')

    context = {'page': page}
    return render(request, 'base/login_register.html', context)


def logout_user(request):
    logout(request)
    return redirect('home')


def user_profile(request, pk):
    user = User.objects.get(id=pk)
    reviews = user.review_set.all()
    review_comments = user.comment_set.all()[0:2]
    context = {
        'user': user,
        'reviews': reviews,
        'review_comments': review_comments,
    }
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            redirect('profile', pk=user.id)

    context = {'form': form}
    return render(request, 'base/update_user.html', context)
