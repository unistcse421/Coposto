from datetime import date

from django import forms
from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

import functions


def upload_to(instance, filename):
    return 'images/%s/%s' % (instance.user.user.username, filename)


class ParcelCategory(models.Model):
    name = models.CharField(max_length=30)


class City(models.Model):
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)


class City_Russian(models.Model):
    id = models.IntegerField(primary_key=True)  # AutoField?
    city = models.TextField(blank=True, null=True)  # This field type is a guess.
    country = models.TextField(blank=True, null=True)  # This field type is a guess.
    hits = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = 'head_city_russian'

    def __unicode__(self):
        return self.city + ', ' + self.country


class Profile(models.Model):
    # user = models.ForeignKey(User, unique=True)
    first_name = models.CharField(max_length=20, default='John')
    last_name = models.CharField(max_length=20, default='Cena')
    email = models.CharField(max_length=20, unique=True,
                             default='user@mail.com')
    password = models.CharField(max_length=128, default='1234')
    passport_number = models.CharField(max_length=20)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], null=True,
                                    blank=True, max_length=20)
                                    # validators should be a list
    is_passport_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    success_rate =  models.FloatField(default=0.0)
    date = models.DateField(default=date.today)

    def __unicode__(self):
        return self.first_name + ', ' + self.email


class Avatar(models.Model):
    """docstring for Avatar"""
    user = models.OneToOneField(Profile, default=0)
    avatar = models.ImageField(upload_to=functions.user_directory_path)


class Parcel(models.Model):
    profile_a = models.ForeignKey(Profile, related_name='profile_a_parcel')
    profile_b = models.ForeignKey(Profile, related_name='profile_b_parcel', blank=True, null=True)
    profiles_b = models.ManyToManyField(Profile, related_name='profiles_b_parcel', blank=True)
    done = models.BooleanField(default=False)
    destination_a = models.ForeignKey(City_Russian, related_name='destination_a_parcel')
    destination_b = models.ForeignKey(City_Russian, related_name='destination_b_parcel')
    date_a = models.DateField()
    date_b = models.DateField()
    parcel_name = models.CharField(max_length=100)
    description = models.TextField(default='')
    price = models.FloatField()
    weight = models.FloatField()
    date = models.DateField(default=date.today)


class Bringer(models.Model):
    profile = models.ForeignKey(Profile, related_name='profile_bringer')
    destination_a = models.ForeignKey(City_Russian, related_name='destination_a_bringer')
    destination_b = models.ForeignKey(City_Russian, related_name='destination_b_bringer')
    flight_date = models.DateField()
    date = models.DateField(default=date.today)


class Review(models.Model):
    profile_a = models.ForeignKey(Profile, related_name='profile_a_review')
    profile_b = models.ForeignKey(Profile, related_name='profile_b_review')
    title = models.CharField(max_length=30)
    text = models.TextField(max_length=200)
    date = models.DateField(default=date.today)


class Image(models.Model):
    item = models.ForeignKey(Parcel, related_name='item_image', default=0)
    image = models.ImageField(upload_to=functions.parcel_image_directory_path)

    # thumbnail = models.ImageField(upload_to='parcel_images/%Y/%m/%d')
    # isthumbnail = models.BooleanField(default=False)
    # def create_thumbnail(self):
    #   # original code for this method came from
    #   # http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/

    #   # If there is no image associated with this.
    #   # do not create thumbnail
    #   if not self.image:
    #       return

    #   from PIL import Image, ImageOps
    #   from cStringIO import StringIO
    #   from django.core.files.uploadedfile import SimpleUploadedFile
    #   import os

    #   # Set our max thumbnail size in a tuple (max width, max height)
    #   THUMBNAIL_SIZE = (288,288)

    #   DJANGO_TYPE = self.image.file.content_type

    #   if DJANGO_TYPE == 'image/jpeg':
    #       PIL_TYPE = 'jpeg'
    #       FILE_EXTENSION = 'jpg'
    #   elif DJANGO_TYPE == 'image/png':
    #       PIL_TYPE = 'png'
    #       FILE_EXTENSION = 'png'

    #   # Open original photo which we want to thumbnail using PIL's Image
    #   image = Image.open(StringIO(self.image.read()))
    #   image_copy = image
    #   # Convert to RGB if necessary
    #   # Thanks to Limodou on DjangoSnippets.org
    #   # http://www.djangosnippets.org/snippets/20/
    #   #
    #   # I commented this part since it messes up my png files
    #   #
    #   #if image.mode not in ('L', 'RGB'):
    #   # image = image.convert('RGB')

    #   # We use our PIL Image object to create the thumbnail, which already
    #   # has a thumbnail() convenience method that contrains proportions.
    #   # Additionally, we use Image.ANTIALIAS to make the image look better.
    #   # Without antialiasing the image pattern artifacts may result.
    #   image = ImageOps.fit(image, THUMBNAIL_SIZE, Image.ANTIALIAS)

    #   # Save the thumbnail
    #   temp_handle = StringIO()
    #   image.save(temp_handle, PIL_TYPE)
    #   temp_handle.seek(0)

    #   # Save image to a SimpleUploadedFile which can be saved into
    #   # ImageField
    #   suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
    #       temp_handle.read(), content_type=DJANGO_TYPE)
    #   # Save SimpleUploadedFile into image field
    #   self.thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)
    #   #=============================================================
    #   NEW_SIZE = (800,800)
    #   image = image_copy
    #   image.thumbnail(NEW_SIZE, Image.ANTIALIAS)

    #   # Save the thumbnail
    #   temp_handle = StringIO()
    #   image.save(temp_handle, PIL_TYPE)
    #   temp_handle.seek(0)

    #   # Save image to a SimpleUploadedFile which can be saved into
    #   # ImageField
    #   suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
    #       temp_handle.read(), content_type=DJANGO_TYPE)
    #   # Save SimpleUploadedFile into image field
    #   self.image.save('%s.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)

    # def save(self):
    #   # create a thumbnail
    #   self.create_thumbnail()

    #   super(Image, self).save()

    # def __unicode__(self):
    #   return smart_unicode(self.item_id)
