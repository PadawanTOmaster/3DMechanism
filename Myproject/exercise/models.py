from django.db import models
from Myproject import settings
import os


class fillblanks(models.Model):
    number = models.IntegerField(primary_key=True)
    problem = models.CharField(max_length=200)
    answere1 = models.CharField(max_length=100, default='')
    answere2 = models.CharField(max_length=100, default='')
    answere3 = models.CharField(max_length=100, default='')
    answere4 = models.CharField(max_length=100, default='')
    answere5 = models.CharField(max_length=100, default='')
    answere6 = models.CharField(max_length=100, default='')
    answere7 = models.CharField(max_length=100, default='')
    answere8 = models.CharField(max_length=100, default='')

    # 填工程制图这种类别 （机械原理）
    keyword1 = models.CharField(max_length=20)
    keyword2 = models.CharField(max_length=20, default='')
    keyword3 = models.CharField(max_length=20, default='')
    # 给答案8个空 3个关键字


class drawing(models.Model):
    number = models.IntegerField(primary_key=True)
    problemtext= models.TextField()
    problemimg=models.FilePathField(path=os.path.join(settings.MEDIA_ROOT, 'images/drawing_pratice'))
    answeretext=models.TextField()
    answereimg=models.FilePathField(path=os.path.join(settings.MEDIA_ROOT, 'images/drawing_pratice'))
    hasthreed = models.IntegerField(default=0)
    keyword1 = models.CharField(max_length=20)
    keyword2 = models.CharField(max_length=20, default='')
    keyword3 = models.CharField(max_length=20, default='')
    type = models.IntegerField()
    # type是类别 尺寸标注类别为1
