# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-06 08:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import head.functions


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0006_auto_20160202_1143'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='image',
            name='isthumbnail',
        ),
        migrations.RemoveField(
            model_name='image',
            name='item_id',
        ),
        migrations.RemoveField(
            model_name='image',
            name='thumbnail',
        ),
        migrations.RemoveField(
            model_name='parcel',
            name='parcel_category',
        ),
        migrations.AddField(
            model_name='image',
            name='item',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='head.Parcel'),
        ),
        migrations.AddField(
            model_name='parcel',
            name='done',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='parcel',
            name='profiles_b',
            field=models.ManyToManyField(blank=True, to='head.Profile'),
        ),
        migrations.AlterField(
            model_name='avatar',
            name='avatar',
            field=models.ImageField(upload_to=head.functions.user_directory_path),
        ),
        migrations.AlterField(
            model_name='avatar',
            name='user',
            field=models.OneToOneField(default=0, on_delete=django.db.models.deletion.CASCADE, to='head.Profile'),
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to=head.functions.parcel_image_directory_path),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='date_a',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='date_b',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='profile_a',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parcel_requests_createdPA', to='head.Profile'),
        ),
        migrations.RemoveField(
            model_name='parcel',
            name='profile_b',
        ),
        migrations.AddField(
            model_name='parcel',
            name='profile_b',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parcel_requests_createdPB', to='head.Profile'),
        ),
    ]
