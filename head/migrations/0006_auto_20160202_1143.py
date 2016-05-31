# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-02 11:43
from __future__ import unicode_literals

from django.db import migrations, models
import head.functions


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0005_avatar_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='avatar',
            name='avatar',
            field=models.FileField(upload_to=head.functions.user_directory_path),
        ),
    ]
