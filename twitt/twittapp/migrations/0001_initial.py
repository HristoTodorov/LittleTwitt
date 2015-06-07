# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('content', models.CharField(max_length=132)),
            ],
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('fallowed', models.IntegerField(unique=True)),
                ('user_fallow', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='profile_images')),
            ],
        ),
        migrations.CreateModel(
            name='Retwit',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('retwiter', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Trend',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('hashtag_content', models.CharField(max_length=132)),
                ('count', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Twitt',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('content', models.CharField(max_length=132)),
                ('date', models.DateField()),
                ('retweet_count', models.IntegerField(default=0)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('picture', models.ForeignKey(blank=True, to='twittapp.Media')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('avatar_id', models.IntegerField(default=1)),
                ('background_id', models.IntegerField(default=1)),
                ('moto', models.CharField(default='', max_length=200)),
                ('country', models.CharField(default='', max_length=100)),
                ('state', models.CharField(default='', max_length=100)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='retwit',
            name='twitt',
            field=models.ForeignKey(to='twittapp.Twitt'),
        ),
        migrations.AddField(
            model_name='comment',
            name='twitt',
            field=models.ForeignKey(to='twittapp.Twitt'),
        ),
        migrations.AddField(
            model_name='comment',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
