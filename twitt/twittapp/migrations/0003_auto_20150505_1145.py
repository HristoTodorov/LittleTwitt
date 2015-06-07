# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twittapp', '0002_auto_20150504_2004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='background_id',
            field=models.IntegerField(default=2),
        ),
    ]
