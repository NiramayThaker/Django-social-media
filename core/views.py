from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post


# Create your views here.
@login_required(login_url='signin')
def index(request):
	# user_obj = User.objects.get(username=request.user.username)
	# profile_data = Profile.objects.get(user=user_obj)
	profile_data = Profile.objects.get(user=request.user.id)

	context = {"profile_data": profile_data}
	return render(request, "index.html", context=context)


@login_required(login_url='signin')
def upload(request):
	if request.method == 'POST':
		user = request.user.username
		image = request.FILES.get('image_upload')
		caption = request.POST['caption']

		new_post = Post.objects.create(user=user, image=image, caption=caption)
		new_post.save()

		return redirect('/')

	return redirect('/')


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
				user_login = auth.authenticate(request, username=username, password=password)
				auth.login(request, user_login)

			# Create profile object for new User
			user_model = User.objects.get(username=username)
			new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
			new_profile.save()

			return redirect('settings')
		else:
			messages.info(request, "Password doesn't match")
			return redirect("signup")

	return render(request, "signup.html")


def signin(request):
	if request.method == "POST":
		username = request.POST["username"]
		password = request.POST["password"]

		user = auth.authenticate(request, username=username, password=password)

		if user is not None:
			auth.login(request, user)
			return redirect('/')
		else:
			messages.info(request, "User Not registered")
			return redirect('signin')

	return render(request, 'signin.html')


@login_required(login_url="signin")
def logout(request):
	print("\n--\n")
	auth.logout(request)
	return redirect('/')


@login_required(login_url="signin")
def settings(request):
	user_profile = Profile.objects.get(user=request.user)

	if request.method == "POST":
		if request.FILES.get('image') is None:
			image = user_profile.profileimg
		elif request.FILES.get('image') is not None:
			image = request.FILES.get('image')

		bio = request.POST['bio']
		location = request.POST['location']

		user_profile.profileimg = image
		user_profile.bio = bio
		user_profile.location = location
		user_profile.save()

		return redirect('settings')

	context = {"user_profile": user_profile}
	return render(request, 'settings.html', context=context)
