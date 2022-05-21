from django.urls import path

from . import views

urlpatterns = [
    # Authentication
    path('register/', views.register_page, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    # Info
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('review/<str:pk>/', views.review, name='review'),
    path('profile/<str:pk>/', views.user_profile, name='profile'),
    # CRUD endpoints
    path('create-review/', views.create_review, name='create-review'),
    path('update-review/<str:pk>/', views.update_review, name='update-review'),
    path('update-comment/<str:pk>/', views.update_comment, name='update-comment'),
    path('delete-review/<str:pk>/', views.delete_review, name='delete-review'),
    path('delete-comment/<str:pk>/', views.delete_comment, name='delete-comment'),
    path('update-user/', views.update_user, name='update-user'),
]
