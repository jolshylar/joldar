from django.urls import path

from . import views

urlpatterns = [
    # Authentication
    path("register/", views.RegisterView.as_view(), name="register"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.LogoutRedirectView.as_view(), name="logout"),
    # Info
    path("", views.HomeView.as_view(), name="home"),
    path("about/", views.AboutView.as_view(), name="about"),
    path("review/<str:pk>/", views.review, name="review"),
    path("profile/<str:pk>/", views.UserProfileDetailView.as_view(), name="profile"),
    # CRUD endpoints
    path("create-review/", views.create_review, name="create-review"),
    path("update-review/<str:pk>/", views.update_review, name="update-review"),
    path("update-comment/<str:pk>/", views.update_comment, name="update-comment"),
    path("delete-review/<str:pk>/", views.delete_review, name="delete-review"),
    path("delete-comment/<str:pk>/", views.delete_comment, name="delete-comment"),
    path("update-user/", views.update_user, name="update-user"),
]
