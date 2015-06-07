# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('twittapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='twitt',
            name='picture',
            field=models.ForeignKey(blank=True, null=True, to='twittapp.Media'),
        ),
    ]
