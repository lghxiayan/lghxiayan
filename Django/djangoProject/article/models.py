from datetime import datetime
from django.utils import timezone

from django.db import models


# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=200)
    password = models.CharField(max_length=200)


class UserExtension(models.Model):
    birthday = models.DateField(null=True, blank=True)
    school = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Tag(models.Model):
    name = models.CharField(max_length=100)


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    pub_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('User', on_delete=models.CASCADE)
    tags = models.ManyToManyField("Tag", blank=True)
