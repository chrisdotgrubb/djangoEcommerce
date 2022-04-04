from django import forms
from localflavor.us.forms import USStateSelect, USZipCodeField, USStateField
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import PhoneNumberField



class PaymentForm(forms.Form):
	name = forms.CharField(label='Name', max_length=150, widget=forms.TextInput(
		attrs={'class': 'form-control', 'placeholder': 'Name', 'id': 'name', 'required': True}))
	
	email = forms.EmailField(label='Email', max_length=200, widget=forms.TextInput(
		attrs={'class': 'form-control', 'placeholder': 'Email', 'id': 'email', 'required': True}))
	
	phone = PhoneNumberField(label='Phone Number', widget=forms.TextInput(
		attrs={'class': 'form-control', 'placeholder': 'Phone number', 'id': 'phone'}))
	
	address = forms.CharField(label='Address', min_length=2, max_length=150, widget=forms.TextInput(
		attrs={'class': 'form-control', 'placeholder': 'Address line 1', 'id': 'address', 'required': True}))
	
	address2 = forms.CharField(label='Apartment Number / Instructions', min_length=2, max_length=150, widget=forms.TextInput(
		attrs={'class': 'form-control', 'placeholder': 'Address line 2', 'id': 'address2'}))
	
	city = forms.CharField(label='Town/City', min_length=2, max_length=150, widget=forms.TextInput(
		attrs={'class': 'form-control', 'placeholder': 'Town/City Name', 'id': 'city', 'required': True}))
	
	country = CountryField(blank=True).formfield(label='Country', widget=CountrySelectWidget(
		attrs={'class': 'form-control', 'placeholder': 'Country', 'id': 'country', 'required': True}, layout='{widget}'))
	
	state = USStateField(widget=USStateSelect(attrs={'class': 'form-control', 'id': 'state', 'required': True}))
	
	zipcode = USZipCodeField(widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'zipcode', 'required': True}))
	
	
	
	


