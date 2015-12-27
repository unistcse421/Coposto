from django import forms

PARCEL_TYPES = [('type1', '< 1kg'), 
				('type2', '1-3kg'),
				('type3', '3-6kg'),
				('type4', '6-10kg'),
				('type5', '> 10kg')]

class Parcel(forms.Form):
	destination_a = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'From', 'class': 'form-control'}))
	destination_b = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'To', 'class': 'form-control'}))
	date_a = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'From', 'class': 'form-control'}))
	date_b = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'To', 'class': 'form-control'}))
	name = forms.CharField(label='', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Parcel name', 'class': 'form-control'}))
	description = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Description', 'class': 'form-control'}))
	weight = forms.FloatField(required=True, label= "", widget=forms.TextInput(attrs={'placeholder': 'Parcel weight in kg', 'class': 'form-control'}))
	price = forms.FloatField(required=True, label= "", widget=forms.TextInput(attrs={'placeholder': 'How much would like to pay?', 'class': 'form-control'}))
	image = forms.ImageField()