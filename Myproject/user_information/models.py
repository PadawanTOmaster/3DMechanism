from django.db import models
from django.contrib.auth.models import AbstractUser
from . import imagestorage
from Myproject import settings
# Create your models here.


class userInfor(AbstractUser):
	username=models.CharField(max_length=40,primary_key=True)
	nickname = models.CharField(max_length=20)
	password=models.CharField(max_length=200)
	email=models.EmailField(blank=True)
	avatar=models.ImageField(upload_to='images/avatar/%Y/%m/%d',storage=imagestorage.ImageStorage(),default='images/avatar/default/originavatar.jpg')
	information=models.TextField(blank=True)
	flag=models.IntegerField(default=2)