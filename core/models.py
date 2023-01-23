from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
class Profile(models.Model):
	# user = pass
	# id_user = pass
	# bio = pass
	profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-photo.png')
	# location = pass

