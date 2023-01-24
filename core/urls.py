from django.urls import path
from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("sign-up", views.signup, name="signup")
]
