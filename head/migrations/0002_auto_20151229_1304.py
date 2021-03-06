# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-29 13:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('head', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=b'parcel_images/%Y/%m/%d')),
                ('thumbnail', models.ImageField(upload_to=b'parcel_images/%Y/%m/%d')),
                ('isthumbnail', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='parcel',
            name='description',
            field=models.CharField(default=b'Best parcel', max_length=200),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='parcel',
            name='weight',
            field=models.FloatField(),
        ),
        migrations.AddField(
            model_name='image',
            name='item_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='head.Parcel'),
        ),
    ]
