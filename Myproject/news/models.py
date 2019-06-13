from django.db import models


# Create your models here.
class schoolnews(models.Model):

    title = models.CharField(max_length=100)
    news_content = models.TextField()
    release_time = models.DateField()
    read_count = models.IntegerField()
    URL = models.CharField(max_length=200)
