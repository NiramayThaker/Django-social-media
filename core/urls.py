from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("settings", views.settings, name="settings"),
	path("sign-up", views.signup, name="signup"),
	path("sign-in", views.signin, name="signin"),
	path("log-out", views.logout, name="logout"),
	path("upload", views.upload, name="upload"),
	path("like-post", views.like_post, name="like-post"),
	path("profile/<str:pk>", views.profile, name="profile"),
]
