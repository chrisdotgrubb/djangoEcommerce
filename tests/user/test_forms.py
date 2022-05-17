from django.test import TestCase
from ecommerce.apps.user.forms import UserLoginForm, RegistrationForm, UserEditForm, UserAddressForm, PwdResetForm, SetPwdForm, PwdChangeForm
from ecommerce.apps.user.models import MyUser


class TestUserLoginForm(TestCase):
	
	def setUp(self):
		self.form = UserLoginForm()
	
	def test_attrs(self):
		for field in self.form.fields:
			self.assertIn('class', self.form.fields[field].widget.attrs)
			self.assertIn('placeholder', self.form.fields[field].widget.attrs)
			self.assertIn('id', self.form.fields[field].widget.attrs)
			self.assertIn('form-control', self.form.fields[field].widget.attrs['class'])
			self.assertIn(f'{field.capitalize()}', self.form.fields[field].widget.attrs['placeholder'])
			self.assertIn(f'login-{field}', self.form.fields[field].widget.attrs['id'])


class TestRegistrationForm(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
		)
		
	def setUp(self):
		self.form = RegistrationForm()
	
	def test_attrs(self):
		for field in self.form.fields:
			self.assertTrue(self.form.fields[field].label)
			self.assertIn('class', self.form.fields[field].widget.attrs)
			self.assertIn('placeholder', self.form.fields[field].widget.attrs)
			self.assertIn('form-control', self.form.fields[field].widget.attrs['class'])
	
	def test_clean_username(self):
		data = {
			'email': 'email2@email.com',
			'username': 'username',
			'first': 'first name',
			'password1': 'GoodPassword000',
			'password2': 'GoodPassword000',
		}
		duplicate = RegistrationForm(data=data)
		self.assertFalse(duplicate.is_valid())
		self.assertEqual(duplicate["username"].errors, ['Username already exists.'])
		
	def test_clean_email(self):
		data = {
			'email': 'email@email.com',
			'username': 'username2',
			'first': 'first name',
			'password1': 'GoodPassword000',
			'password2': 'GoodPassword000',
		}
		duplicate = RegistrationForm(data=data)
		self.assertFalse(duplicate.is_valid())
		self.assertEqual(duplicate["email"].errors, ['Email already exists.'])
		
	def test_clean_password2(self):
		data = {
			'email': 'email2@email.com',
			'username': 'username2',
			'first': 'first name',
			'password1': 'GoodPassword000',
			'password2': 'GoodPassword111',
		}
		duplicate = RegistrationForm(data=data)
		self.assertFalse(duplicate.is_valid())
		self.assertEqual(duplicate["password2"].errors, ['Passwords do not match.'])
		
		