from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from head.models import Parcel, City
from head.functions import home_context

PARCEL_TYPES = [('type1', '< 1kg'), 
				('type2', '1-3kg'),
				('type3', '3-6kg'),
				('type4', '6-10kg'),
				('type5', '> 10kg')]

class ParcelForm(ModelForm):
	class Meta:
		model = Parcel
		# fields = ['destination_a', 'destination_b', 'date_a', 'date_b', 'parcel_name', 'description', 'weight', 'price']
		exclude = ['profile_a', 'profile_b', 'parcel_category']
		widgets = {
            'destination_a' : forms.TextInput(attrs={'placeholder': home_context['from_dest'], 'class': 'form-control', 'required': 'true', 'data-remote': '/send_form_validator/'}),
            'destination_b' : forms.TextInput(attrs={'placeholder': home_context['to_dest'], 'class': 'form-control', 'required': 'true', 'data-remote': '/send_form_validator/'}),
            'date_a' : forms.TextInput(attrs={'placeholder': home_context['from_date'], 'class': 'form-control', 'required': 'true', 'data-remote': '/send_form_validator/'}),
            'date_b' : forms.TextInput(attrs={'placeholder': home_context['to_date'], 'class': 'form-control', 'required': 'true', 'data-remote': '/send_form_validator/'}),
            'parcel_name' : forms.TextInput(attrs={'placeholder': home_context['parcel_name'], 'class': 'form-control', 'required': 'true', 'data-remote': '/send_form_validator/'}),
            'description' : forms.Textarea(attrs={'placeholder': home_context['parcel_description'], 'class': 'form-control', 'required': 'true', 'data-remote': '/send_form_validator/'}),
            'weight' : forms.TextInput(attrs={'placeholder': home_context['weight'], 'class': 'form-control', 'required': 'true', 'data-remote': '/send_form_validator/'}),
            'price' : forms.TextInput(attrs={'placeholder': home_context['price'], 'class': 'form-control', 'required': 'true', 'data-remote': '/send_form_validator/'})
        }
	
	image = forms.ImageField()

	error_css_class = 'error'

class RegistrationFormUniqueEmail(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'first_name', 'last_name', 'email']
	image = forms.ImageField()

		