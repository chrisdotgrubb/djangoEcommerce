import uuid
import phonenumbers
from django.core.mail import send_mail
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField
from phonenumber_field.modelfields import PhoneNumberField


class AccountManager(BaseUserManager):
	
	def create_user(self, email, username, password, **other_fields):
		if not email:
			raise ValueError(_('Email address required.'))
		if not username:
			raise ValueError(_('Username required.'))
		if not password:
			raise ValueError(_('Password required.'))
		
		email = self.normalize_email(email)
		user = self.model(email=email, username=username, **other_fields)
		user.set_password(password)
		user.save()
		return user
		
		
	def create_superuser(self, email, username, password, **other_fields):
		other_fields.setdefault('is_active', True)
		other_fields.setdefault('is_staff', True)
		other_fields.setdefault('is_superuser', True)
		return self.create_user(email, username, password, **other_fields)
		

class ActiveUserManager(models.Manager):
	
	def get_queryset(self):
		return super().get_queryset().filter(is_active=True)


class InactiveUserManager(models.Manager):
	
	def get_queryset(self):
		return super().get_queryset().filter(is_active=False)
	
	
class MyUser(AbstractBaseUser, PermissionsMixin):
	
	email = models.EmailField(_('email address'), unique=True)
	username = models.CharField(max_length=150, unique=True)
	phone = PhoneNumberField(blank=True)
	first = models.CharField(max_length=150, blank=True)
	
	is_active = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']
	
	objects = AccountManager()
	active = ActiveUserManager()
	inactive = InactiveUserManager()
	
	class Meta:
		verbose_name = 'Accounts'
		verbose_name_plural = 'Accounts'
		
	def __str__(self):
		return self.username
	
	def email_user(self, subject, message):
		send_mail(subject, message, 'from@email.com', [self.email], fail_silently=False)
	

class Address(models.Model):
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	customer = models.ForeignKey(MyUser, verbose_name=_('Customer'), on_delete=models.CASCADE)
	
	name = models.CharField(_('Full Name'), max_length=150)
	phone = PhoneNumberField(blank=True)
	country = CountryField(blank=True)
	address_line_1 = models.CharField(max_length=150, blank=True)
	address_line_2 = models.CharField(max_length=150, blank=True)
	town_city = models.CharField(max_length=150, blank=True)
	zip = models.CharField(_('Zipcode'), max_length=13)
	delivery_instructions = models.CharField(_('Delivery instructions'), max_length=255)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	default = models.BooleanField(_('Default'), default=False)
	
	class Meta:
		verbose_name = 'Address'
		verbose_name_plural = 'Addresses'
		
	def __str__(self):
		return f'{self.name} address'
	
	def formatted_phone(self):
		return phonenumbers.format_number(self.phone, phonenumbers.PhoneNumberFormat.NATIONAL)
