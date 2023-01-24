from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile


# Create your views here.
@login_required()
def index(request):
	return render(request, "index.html")


def signup(request):
	if request.method == "POST":
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		password2 = request.POST['password2']

		if password == password2:
			if User.objects.filter(email=email).exists() or User.objects.filter(username=username).exists():
				messages.info(request, "Email or Username already Exists")
				return redirect("signup")
			else:
				user = User.objects.create_user(username=username,
												email=email,
												password=password)
				user.save()
			# Log user in and redirect to settings page

			# Create profile object for new User
			user_model = User.objects.get(username=username)
			new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
			new_profile.save()

			return redirect('signup')
		else:
			messages.info(request, "Password doesn't match")
			return redirect("signup")

	return render(request, "signup.html")


def signin(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]

		user = auth.authenticate(username=username, password=password)

		if user is None:
			messages.info(request, "User Not registered")
			return redirect('signin')
		else:
			auth.login(request, user)
			return redirect('/')

	return render(request, 'signin.html')


def logout(request):
	auth.logout(request)
	return render('/')
