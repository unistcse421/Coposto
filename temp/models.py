from django.db import models

class City(models.Model):
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)

class Profile(models.Model):
	firstName = models.CharField(max_length=30)
	lastName = models.CharField(max_length=30)
	email = models.EmailField(max_length=70, blank=True, null=True, unique=True)
	passport_number = models.CharField(max_length=20)
	phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], blank=True) # validators should be a list
    is_verified = models.BooleanField(default=False)
    success_rate =  models.FloatField(default=0.0)

class Parcel(models.Model):
	profile_a = models.ForeignKey(Profile)
	profile_b = models.ManyToManyField(Profile)
	destination_a = models.ForeignKey(City)
	destination_b = models.ForeignKey(City)
	date_a = models.DateTimeField(blank=False)
	date_b = models.DateTimeField(blank=False)
	parcel_name = models.CharField(max_length=100)
	parcel_category = models.ForeignKey(ParcelCategory)
	price = models.FloatField(default=0.0)
	weight = models.FloatField(default=0.0)

class ParcelCategory(models.Model):
	name = models.CharField(max_length=30)

class Review(models.Model):
	profile_a = models.ForeignKey(Profile)
	profile_b = models.ForeignKey(Profile)
	title = models.CharField(max_length=30)
	text = models.TextField(max_length=200)
	date = models.DateTimeField(auto_now_add=True)
