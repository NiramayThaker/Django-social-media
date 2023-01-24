from django.db import models
from django.contrib.auth import get_user_model

# Will get all the currently authenticated User
User = get_user_model()


# Create your models here.
class Profile(models.Model):
	# Assigning Foreign Key to user Filed of profile model to User(django) model
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	id_user = models.IntegerField()

	# Ok if user doesn't want to set any BIO
	bio = models.TextField(blank=True)

	# Field to save image in profile image folder child of Media Folder
	profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-photo.png')

	#
	location = models.CharField(max_length=100, blank=True)

	def __str__(self):
		# Initializing Dunder method to print UserName on admin panel
		return self.user.username
