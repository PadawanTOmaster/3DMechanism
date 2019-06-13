from django.db import models

# Create your models here.
class encyclopedia(models.Model):
	title=models.TextField()
	context=models.TextField()