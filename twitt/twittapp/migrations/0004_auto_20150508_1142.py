# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twittapp', '0003_auto_20150505_1145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='media',
            name='picture',
            field=models.ImageField(upload_to='/home/hristo/littleTwitt/twitt/twittapp/static/media'),
        ),
        migrations.AlterField(
            model_name='twitt',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
