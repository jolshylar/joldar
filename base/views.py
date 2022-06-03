from typing import Any, Dict, Optional

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
# Class-based Views
from django.views import View
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

# Local imports
from base.forms import CustomUserCreationForm, ReviewForm, UserForm
from base.models import Comment, Review, User


class HomeView(ListView):
    model = Review
    template_name: str = "base/home.html"
    paginate_by: int = 5

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["all_reviews"] = Review.objects.all()
        return context


def review(request, pk):
    review = Review.objects.get(id=pk)
    review_comments = review.comment_set.all()

    if request.method == "POST":
        Comment.objects.create(
            body=request.POST.get("body"),
            author=request.user,
            review=review,
        )
        return redirect("review", pk=review.id)

    context = {
        "review": review,
        "review_comments": review_comments,
    }
    return render(request, "base/review.html", context)


# ===== REVIEW CRUD =====
@login_required(login_url="login")
def create_review(request):
    state = "Create"
    form = ReviewForm()
    if request.method == "POST":
        Review.objects.create(
            title=request.POST.get("title"),
            summary=request.POST.get("summary"),
            body=request.POST.get("body"),
            author=request.user,
        )
        return redirect("home")

    context = {"form": form, "state": state}
    return render(request, "base/review_form.html", context)


@login_required(login_url="login")
def update_review(request, pk):
    state = "Update"
    review = Review.objects.get(id=pk)
    form = ReviewForm(instance=review)

    if request.user != review.author:
        return HttpResponse(_("You are not allowed here!"))

    if request.method == "POST":
        review.title = request.POST.get("title")
        review.summary = request.POST.get("summary")
        review.body = request.POST.get("body")
        review.save()
        return redirect("home")

    context = {"form": form, "review": review, "state": state}
    return render(request, "base/review_form.html", context)


@login_required(login_url="login")
def update_comment(request, pk):
    comment = Comment.objects.get(id=pk)
    old_body = comment.body

    if request.user != comment.author:
        return HttpResponse(_("You are not allowed here!"))

    if request.method == "POST":
        comment.body = request.POST.get("body")
        comment.save()
        return redirect("review", pk=comment.review.id)

    context = {"old_body": old_body}
    return render(request, "base/update_comment.html", context)


@login_required(login_url="login")
def delete_review(request, pk):
    review = Review.objects.get(id=pk)

    if request.user != review.author:
        return HttpResponse(_("You are not allowed here!"))

    if request.method == "POST":
        review.delete()
        return redirect("home")

    context = {"obj": review}
    return render(request, "base/delete.html", context)


@login_required(login_url="login")
def delete_comment(request, pk):
    comment = Comment.objects.get(id=pk)

    if request.user != comment.author:
        return HttpResponse(_("You are not allowed here!"))

    if request.method == "POST":
        comment.delete()
        # TODO: think whether to redirect to a parent comment or home
        return redirect("review", comment.review.id)

    context = {"obj": comment}
    return render(request, "base/delete.html", context)


class AboutView(TemplateView):
    template_name: str = "base/about.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        with open(settings.MARKDOWN_ROOT / "about.md", "r") as f:
            context["markdown_content"] = f.read()
        return context


# ===== AUTHENTICATION =====
class RegisterView(View):
    """A class-based view used for `/register/`"""

    def get(self, request):
        form = CustomUserCreationForm()
        context = {"form": form}
        return render(request, "base/login_register.html", context)

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Login after registration
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, _("An error occurred during registration"))
            return redirect("register")


class LoginView(View):
    """A class-based view used for `/login/`"""

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("home")

        context = {"page": "login"}
        return render(request, "base/login_register.html", context)

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, _("User does not exist"))

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, _("Email or Password entered wrong"))
            return redirect("login")


class LogoutRedirectView(RedirectView):
    pattern_name: Optional[str] = "home"

    def get_redirect_url(self, *args: Any, **kwargs: Any) -> Optional[str]:
        logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class UserProfileDetailView(DetailView):
    model = get_user_model()
    template_name: str = "base/profile.html"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        user = User.objects.get(id=self.kwargs.get("pk"))
        context = super().get_context_data(**kwargs)
        context["user"] = user
        context["latest_review"] = user.review_set.first()
        context["review_comments"] = user.comment_set.all()[0:2]
        return context


@login_required(login_url="login")
def update_user(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("profile", pk=user.id)

    context = {"form": form}
    return render(request, "base/update_user.html", context)
