from django.db import models
from . import filesstorage
# Create your models here.
class download(models.Model):
	filepath=models.FileField(upload_to='files/download',storage=filesstorage.FilesStorage())
	imgpath=models.ImageField(upload_to='files/download',storage=filesstorage.ImageStorage())
	filename=models.CharField(max_length=50)
	description=models.TextField()
	# 对该文件的描述
