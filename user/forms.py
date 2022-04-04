from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm, SetPasswordForm, PasswordChangeForm
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from phonenumber_field.formfields import PhoneNumberField

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
			{'class': 'form-control', 'placeholder': 'Username', 'hx-post': "/user/check_username/", 'hx-swap': "outerHTML", 'hx-trigger': "keyup changed delay:500ms", 'hx-target': "#username-error"})
		self.fields['email'].widget.attrs.update(
			{'class': 'form-control', 'placeholder': 'E-mail', 'hx-post': "/user/check_email/", 'hx-swap': "outerHTML", 'hx-trigger': "keyup changed delay:500ms", 'hx-target': "#email-error"})
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


class UserEditForm(forms.ModelForm):
	email = forms.EmailField(label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
		attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email', 'readonly': 'readonly', 'style': 'cursor:not-allowed'}))
	
	username = forms.CharField(label='Username (can not be changed)', min_length=4, max_length=50, widget=forms.TextInput(
		attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-username', 'readonly': 'readonly', 'style': 'cursor:not-allowed'}))
	
	first = forms.CharField(label='First name', min_length=2, max_length=50, widget=forms.TextInput(
		attrs={'class': 'form-control mb-3', 'placeholder': 'First name', 'id': 'form-first'}))
	
	country = CountryField(blank=True).formfield(label='Country', widget=CountrySelectWidget(
		attrs={'class': 'form-control mb-3', 'placeholder': 'Country', 'id': 'form-country'}, layout='{widget}'))
	
	phone = PhoneNumberField(label='phone', widget=forms.TextInput(
		attrs={'class': 'form-control mb-3', 'placeholder': 'Phone number', 'id': 'form-phone'}))
	
	address_line_1 = forms.CharField(label='Address', min_length=2, max_length=150, widget=forms.TextInput(
		attrs={'class': 'form-control mb-3', 'placeholder': 'Address line 1', 'id': 'form-address1'}))
	
	address_line_2 = forms.CharField(label='Address continued', min_length=2, max_length=150, widget=forms.TextInput(
		attrs={'class': 'form-control mb-3', 'placeholder': 'Address line 2', 'id': 'form-address2'}))
	
	town_city = forms.CharField(label='Town/City', min_length=2, max_length=150, widget=forms.TextInput(
		attrs={'class': 'form-control mb-3', 'placeholder': 'Town/City', 'id': 'form-town'}))
	
	about = forms.CharField(label='About me', min_length=2, max_length=500, widget=forms.Textarea(
		attrs={'class': 'form-control mb-3', 'placeholder': 'About me', 'id': 'form-about'}))
	
	class Meta:
		model = MyUser
		fields = ['email', 'username', 'first', 'country', 'phone', 'address_line_1', 'address_line_2', 'town_city', 'about']
	
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['username'].required = True
		self.fields['email'].required = True
		self.fields['first'].required = False
		self.fields['country'].required = False
		self.fields['phone'].required = False
		self.fields['address_line_1'].required = False
		self.fields['address_line_2'].required = False
		self.fields['town_city'].required = False
		self.fields['about'].required = False


class PwdResetForm(PasswordResetForm):
	email = forms.EmailField(max_length=254, widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Email', 'id': 'form-email'}))
	
	def clean_email(self):
		email = self.cleaned_data['email']
		user = MyUser.objects.filter(email__iexact=email)
		if not user:
			raise forms.ValidationError('That email was not found. Please recheck the spelling.')
		return email


class SetPwdForm(SetPasswordForm):
	new_password1 = forms.CharField(
		label='New password:',
		widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass1'}),
		strip=False,
		help_text=password_validation.password_validators_help_text_html(),
	)
	new_password2 = forms.CharField(
		label='New password again:',
		strip=False,
		widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'New Password again', 'id': 'form-new-pass2'}),
	)


class PwdChangeForm(PasswordChangeForm):
	old_password = forms.CharField(
		label="Old password:",
		strip=False,
		widget=forms.PasswordInput(
			attrs={'class': 'form-control mb-3', 'placeholder': 'Old Password', 'id': 'form-old-pass', 'autofocus': True}
		),
	)
	new_password1 = forms.CharField(
		label="New password:",
		widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'New Password', 'id': 'form-new-pass1'}),
		strip=False,
		help_text=password_validation.password_validators_help_text_html(),
	)
	new_password2 = forms.CharField(
		label="New password again:",
		strip=False,
		widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'New Password again', 'id': 'form-new-pass2'}),
	)
