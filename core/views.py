import random
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Post, LikePost, Followers
from itertools import chain


# Create your views here.
@login_required(login_url='signin')
def index(request):
	# user_obj = User.objects.get(username=request.user.username)
	# profile_data = Profile.objects.get(user=user_obj)
	profile_data = Profile.objects.get(user=request.user.id)
	
	user_following_list = []
	feed = []

	user_following = Followers.objects.filter(follower=request.user.username)
	for user in user_following:
		user_following_list.append(user)
	
	for user_name in user_following_list:
		feed_list = Post.objects.filter(user=user_name)
		feed.append(feed_list)
	
	feed_list = list(chain(*feed))

	# User Suggestions Section
	all_users = User.objects.all()
	curr_user = User.objects.filter(username=request.user.username)
	user_following_all = [] + curr_user

	for user in user_following:
		user_list = User.objects.get(username=user.user)
		user_following_all.append(user_list)

	suggestion_list = [x for x in list(all_users) if (x not in list(user_following_all))]
	random.shuffle(suggestion_list)

	username_profile = []
	username_profile_list = []

	for users in suggestion_list:
		username_profile.append(user.id)

	for ids in username_profile:
		profile_list = Profile.objects.filter(id_user=ids)
		username_profile_list.append(profile_list)

	suggestion_username_profile_list = list(chain(*username_profile_list))

	context = {"profile_data": profile_data, "posts": feed_list, "suggestion_username_profile_list": suggestion_username_profile_list}
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


@login_required(login_url='signin')
def profile(request, pk):
	user_obj = User.objects.get(username=pk)
	user_profile = Profile.objects.get(user=user_obj)
	user_posts = Post.objects.filter(user=pk)
	user_post_len = len(user_posts)
	followers = Followers.objects.filter(user=pk)
	following = Followers.objects.filter(follower=pk)

	follower_ = request.user.username
	user = pk
	if Followers.objects.filter(follower=follower_, user=user):
		button_text = "Unfollow"
	else:
		button_text = "Follow"

	context = {"user_profile": user_profile,
			   "user_obj": user_obj,
			   "user_posts": user_posts,
			   "user_post_len": user_post_len,
			   "followers": followers,
			   "follower_len": len(followers),
			   "following_len": len(following),
			   "button_text": button_text,
			   }

	return render(request, 'profile.html', context=context)


@login_required(login_url="signin")
def like_post(request):
	username = request.user.username
	post_id = request.GET.get('post-id')
	post = Post.objects.get(id=post_id)
	like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

	if like_filter is None:
		new_like = LikePost.objects.create(post_id=post_id, username=username)
		new_like.save()
		post.no_of_likes += 1
		post.save()
		return redirect('/')
	else:
		like_filter.delete()
		post.no_of_likes -= 1
		post.save()
		return redirect('/')


@login_required(login_url="signin")
def follow(request):
	if request.method == "POST":
		follower = request.POST['follower']
		user = request.POST['user']

		if Followers.objects.filter(follower=follower, user=user).first():
			delete_follower = Followers.objects.get(follower=follower, user=user)
			delete_follower.delete()
			return redirect(f'/profile/{user}')
		else:
			new_follower = Followers.objects.create(follower=follower, user=user)
			new_follower.save()
			return redirect(f'/profile/{user}')
	else:
		return redirect("/")


def search(request):
	user_object = User.objects.get(username=request.user.username)
	user_profile = Profile.objects.get(user=user_object)
	if request.method == "POST":
		username = request.POST['username']
		username_object = User.objects.filter(username__icontains=username)
		username_profile = []
		username_profile_list = []

		for users in username_object:
			username_profile.append(users.id)

		for ids in username_profile:
			profile_lists = Profile.objects.filter(id_user=ids)
			username_profile_list.append(profile_lists)

		username_profile_list = list(chain(*username_profile_list))

	context = {"user_object": user_object, "user_profile": user_profile, "username_profile_list": username_profile_list}
	return render(request, "search.html", context=context)


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


