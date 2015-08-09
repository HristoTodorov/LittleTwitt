from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from twitt.settings import MEDIA_ROOT


class Media(models.Model):
    picture = models.ImageField(upload_to=MEDIA_ROOT)


class UserProfile(models.Model):
    user = models.ForeignKey(User)
    avatar_id = models.IntegerField(default=1)
    background_id = models.IntegerField(default=2)
    moto = models.CharField(max_length=200, default='')
    country = models.CharField(max_length=100, default='')
    state = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.user


class Twitt(models.Model):
    author = models.ForeignKey(User, blank=False)
    content = models.CharField(max_length=255, blank=True, default='')
    date = models.DateField(auto_now_add=True, editable=False, blank=True)
    retweet_count = models.IntegerField(default=0)


class Comment(models.Model):
    user = models.ForeignKey(User)
    twitt = models.ForeignKey(Twitt)
    content = models.CharField(max_length=132)


class Follower(models.Model):
    followed = models.IntegerField(unique=True, blank=False)
    user_follow = models.IntegerField(unique=True, blank=False)


class Trend(models.Model):
    content = models.CharField(max_length=132)
    count = models.IntegerField()


class Retwitt(models.Model):
    twitt_id = models.IntegerField()
    retwitter_id = models.IntegerField()


class HashtagedTwitt(models.Model): 
    twitt_id = models.IntegerField()
    hashtag_id = models.IntegerField()
