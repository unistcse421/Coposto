# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-14 06:28
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0008_auto_20160212_1648'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
