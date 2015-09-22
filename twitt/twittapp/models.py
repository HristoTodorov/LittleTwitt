from django.db import models
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.conf import settings
from twitt.settings import MEDIA_ROOT


class Media(models.Model):
    picture = models.ImageField(upload_to=MEDIA_ROOT)


class UserProfile(models.Model):
    avatar_id = models.IntegerField(default=1)
    background_id = models.IntegerField(default=2)
    moto = models.CharField(max_length=200, default='')
    country = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')
    follower = models.ManyToManyField(User)
    followers = models.IntegerField(default=0)

    def __str__(self):
        return self.user


class Twitt(models.Model):
    author = models.ForeignKey(User, blank=False)
    content = models.CharField(max_length=255, blank=True, default='')
    date = models.DateField(auto_now_add=True, editable=False, blank=True)
    retweet_count = models.IntegerField(default=0)
    retweeter = models.ManyToManyField(UserProfile)


class Comment(models.Model):
    user = models.ForeignKey(User)
    twitt = models.ForeignKey(Twitt)
    content = models.CharField(max_length=132)


class Trend(models.Model):
    content = models.CharField(max_length=132)
    count = models.IntegerField()
    twitt = models.ManyToManyField(Twitt)
