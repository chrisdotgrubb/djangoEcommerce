from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm
from .models import MyUser


class UserLoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'login-username'}))
	password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'id': 'login-password'}))
	
	
class RegistrationForm(forms.ModelForm):

	username = forms.CharField(label='Enter Username: ', min_length=4, max_length=50, help_text='Required')
	email = forms.EmailField(label='Email: ', max_length=100, help_text='Required', error_messages={'required': 'Email is required.'})
	password1 = forms.CharField(label='Password: ', widget=forms.PasswordInput, help_text=password_validation.password_validators_help_text_html)
	password2 = forms.CharField(label='Password again: ', widget=forms.PasswordInput)
	
	class Meta:
		model = MyUser
		fields = ['username', 'email']
		
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].widget.attrs.update(
			{'class': 'form-control mb-3', 'placeholder': 'Username'})
		self.fields['email'].widget.attrs.update(
			{'class': 'form-control mb-3', 'placeholder': 'E-mail'})
		self.fields['password1'].widget.attrs.update(
			{'class': 'form-control mb-3', 'placeholder': 'Password'})
		self.fields['password2'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': 'Password again'})
		
		
	def clean_username(self):
		username = self.cleaned_data['username']
		if MyUser.objects.filter(username__iexact=username).exists():
			raise forms.ValidationError('Username already exists.')
		return username
	
	def clean_password2(self):
		cd = self.cleaned_data
		if cd['password1'] != cd['password2']:
			raise forms.ValidationError('Passwords do not match.')
		password_validation.validate_password(cd['password2'], None)
		return cd['password2']
	
	def clean_email(self):
		email = self.cleaned_data['email']
		if MyUser.objects.filter(email__iexact=email).exists():
			raise forms.ValidationError('Email already exists.')
		return email
		