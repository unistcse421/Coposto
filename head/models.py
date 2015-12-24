from django.db import models
from django.core.validators import RegexValidator


def upload_to(instance, filename):
    return 'images/%s/%s' % (instance.user.user.username, filename)

class ParcelCategory(models.Model):
	name = models.CharField(max_length=30)

class City(models.Model):
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)

class Profile(models.Model):
	firstName = models.CharField(max_length=30)
	lastName = models.CharField(max_length=30)
	email = models.EmailField(max_length=70, blank=True, null=True, unique=True)
	passport_number = models.CharField(max_length=20)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
	phone_number = models.CharField(validators=[phone_regex], blank=True, max_length=20) # validators should be a list
	is_verified = models.BooleanField(default=False)
	success_rate =  models.FloatField(default=0.0)

class Parcel(models.Model):
	profile_a = models.ForeignKey(Profile, related_name='%(class)s_requests_created')
	profile_b = models.ManyToManyField(Profile)
	destination_a = models.ForeignKey(City, related_name='%(class)s_requests_createdA')
	destination_b = models.ForeignKey(City, related_name='%(class)s_requests_createdB')
	date_a = models.DateTimeField(blank=False)
	date_b = models.DateTimeField(blank=False)
	parcel_name = models.CharField(max_length=100)
	parcel_category = models.ForeignKey(ParcelCategory, related_name='%(class)s_requests_created')
	price = models.FloatField(default=0.0)
	weight = models.FloatField(default=0.0)

class Review(models.Model):
	profile_a = models.ForeignKey(Profile, related_name='%(class)s_requests_createdA')
	profile_b = models.ForeignKey(Profile, related_name='%(class)s_requests_createdB')
	title = models.CharField(max_length=30)
	text = models.TextField(max_length=200)
	date = models.DateTimeField(auto_now_add=True)

class Image(models.Model):
	item_id = models.ForeignKey(Parcel, blank=True, null=True)
	image = models.ImageField(upload_to='parcel_images/%Y/%m/%d')
	thumbnail = models.ImageField(upload_to='parcel_images/%Y/%m/%d')
	isthumbnail = models.BooleanField(default=False)
	def create_thumbnail(self):
		# original code for this method came from
		# http://snipt.net/danfreak/generate-thumbnails-in-django-with-pil/
		 
		# If there is no image associated with this.
		# do not create thumbnail
		if not self.image:
			return
		 
		from PIL import Image, ImageOps
		from cStringIO import StringIO
		from django.core.files.uploadedfile import SimpleUploadedFile
		import os
		 
		# Set our max thumbnail size in a tuple (max width, max height)
		THUMBNAIL_SIZE = (288,288)
		 
		DJANGO_TYPE = self.image.file.content_type
		 
		if DJANGO_TYPE == 'image/jpeg':
			PIL_TYPE = 'jpeg'
			FILE_EXTENSION = 'jpg'
		elif DJANGO_TYPE == 'image/png':
			PIL_TYPE = 'png'
			FILE_EXTENSION = 'png'
		 
		# Open original photo which we want to thumbnail using PIL's Image
		image = Image.open(StringIO(self.image.read()))
		image_copy = image 
		# Convert to RGB if necessary
		# Thanks to Limodou on DjangoSnippets.org
		# http://www.djangosnippets.org/snippets/20/
		#
		# I commented this part since it messes up my png files
		#
		#if image.mode not in ('L', 'RGB'):
		# image = image.convert('RGB')
		 
		# We use our PIL Image object to create the thumbnail, which already
		# has a thumbnail() convenience method that contrains proportions.
		# Additionally, we use Image.ANTIALIAS to make the image look better.
		# Without antialiasing the image pattern artifacts may result.
		image = ImageOps.fit(image, THUMBNAIL_SIZE, Image.ANTIALIAS)
		 
		# Save the thumbnail
		temp_handle = StringIO()
		image.save(temp_handle, PIL_TYPE)
		temp_handle.seek(0)
		 
		# Save image to a SimpleUploadedFile which can be saved into
		# ImageField
		suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
			temp_handle.read(), content_type=DJANGO_TYPE)
		# Save SimpleUploadedFile into image field
		self.thumbnail.save('%s_thumbnail.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)
		#=============================================================
		NEW_SIZE = (800,800)
		image = image_copy
		image.thumbnail(NEW_SIZE, Image.ANTIALIAS)
		 
		# Save the thumbnail
		temp_handle = StringIO()
		image.save(temp_handle, PIL_TYPE)
		temp_handle.seek(0)
		 
		# Save image to a SimpleUploadedFile which can be saved into
		# ImageField
		suf = SimpleUploadedFile(os.path.split(self.image.name)[-1],
			temp_handle.read(), content_type=DJANGO_TYPE)
		# Save SimpleUploadedFile into image field
		self.image.save('%s.%s'%(os.path.splitext(suf.name)[0],FILE_EXTENSION), suf, save=False)

	def save(self):
		# create a thumbnail
		self.create_thumbnail()
		
		super(Image, self).save()

	def __unicode__(self):
		return smart_unicode(self.item_id)





