from django import forms

PARCEL_TYPES = [('type1', '< 1kg'), 
				('type2', '1-3kg'),
				('type3', '3-6kg'),
				('type4', '6-10kg'),
				('type5', '> 10kg')]

class Parcel(forms.Form):
    destination_a = forms.CharField(label='From', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'From'}))
    destination_b = forms.CharField(label='To', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'To'}))
    name = forms.CharField(label='Name', max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Parcel name'}))
    description = forms.Textarea(attrs={'placeholder': 'Description'}))
	weight = forms.FloatField(required=True, label= "Parcel weight", widget=forms.TextInput(attrs={'placeholder': 'Parcel weight in kg'}))
	price = forms.FloatField(required=True, label= "Suggested price", widget=forms.TextInput(attrs={'placeholder': 'How much would like to pay?'}))
	image = forms.ImageField()