from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill, ResizeToFit, Thumbnail

# Create your models here.

class User(AbstractUser):
	followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="followings")
	image = ProcessedImageField(
		processors=[ResizeToFill(100, 100)],
		format='JPEG',
		options={'quality': 100},
		blank=True,
		default='profile_img.png')
	introduction = models.CharField(max_length=500, blank=True)
