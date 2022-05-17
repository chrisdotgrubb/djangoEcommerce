from django.test import TestCase
from ecommerce.apps.user.forms import UserLoginForm, RegistrationForm, UserEditForm, UserAddressForm, PwdResetForm, SetPwdForm, PwdChangeForm
from ecommerce.apps.user.models import MyUser


class TestUserLoginForm(TestCase):
	
	def setUp(self):
		self.form = UserLoginForm()
	
	def test_attrs(self):
		self.assertEqual('Email', self.form.fields['username'].widget.attrs['placeholder'])
		self.assertEqual('Password', self.form.fields['password'].widget.attrs['placeholder'])
		self.assertEqual('login-email', self.form.fields['username'].widget.attrs['id'])
		self.assertEqual('login-password', self.form.fields['password'].widget.attrs['id'])
		
		for field in self.form.fields:
			self.assertIn('class', self.form.fields[field].widget.attrs)
			self.assertIn('placeholder', self.form.fields[field].widget.attrs)
			self.assertIn('id', self.form.fields[field].widget.attrs)
			self.assertIn('form-control', self.form.fields[field].widget.attrs['class'])
	
	def test_field_length(self):
		self.assertEqual(len(self.form.fields), 2)
	
	def test_form_is_valid(self):
		user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
		)
		data = {
			'username': 'email@email.com',
			'password': 'GoodPassword000',
		}
		form = UserLoginForm(data=data)
		self.assertTrue(form.is_valid())
		self.assertEqual(len(form.errors), 0)


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
	
	def test_form_is_valid(self):
		data = {
			'email': 'email2@email.com',
			'username': 'username2',
			'first': 'first name',
			'password1': 'GoodPassword000',
			'password2': 'GoodPassword000',
		}
		form = RegistrationForm(data=data)
		self.assertTrue(form.is_valid())
		self.assertEqual(len(form.errors), 0)
	
	def test_field_length(self):
		self.assertEqual(len(self.form.fields), 4)


class TestUserEditForm(TestCase):
	
	def setUp(self):
		self.form = UserEditForm()
	
	def test_attrs(self):
		for field in self.form.fields:
			self.assertIn('class', self.form.fields[field].widget.attrs)
			self.assertIn('placeholder', self.form.fields[field].widget.attrs)
			self.assertIn('id', self.form.fields[field].widget.attrs)
			self.assertIn('form-control', self.form.fields[field].widget.attrs['class'])
			self.assertIn(f'{field.capitalize()}', self.form.fields[field].widget.attrs['placeholder'])
			self.assertIn(f'form-{field}', self.form.fields[field].widget.attrs['id'])
	
	def test_readonly(self):
		self.assertIn('readonly', self.form.fields['email'].widget.attrs['readonly'])
		self.assertIn('readonly', self.form.fields['username'].widget.attrs['readonly'])
	
	def test_form_is_valid(self):
		user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
		)
		data = {
			'email': 'email@email.com',
			'username': 'username',
			'first': 'first',
			'phone': '(814) 574-0000',
		}
		form = UserEditForm(instance=user, data=data)
		self.assertTrue(form.is_valid())
		self.assertEqual(len(form.errors), 0)
	
	def test_field_length(self):
		self.assertEqual(len(self.form.fields), 4)


class TestUserAddressForm(TestCase):
	
	def setUp(self):
		self.form = UserAddressForm()
	
	def test_attrs(self):
		for field in self.form.fields:
			self.assertIn('class', self.form.fields[field].widget.attrs)
			self.assertIn('form-control', self.form.fields[field].widget.attrs['class'])
			self.assertIn('account-form', self.form.fields[field].widget.attrs['class'])
	
	def test_form_is_valid(self):
		data = {
			'name': 'one',
			'phone': '(814)574-0000',
			'country': 'US',
			'address_line_1': '123 Main Street',
			'address_line_2': 'Apartment 2',
			'town_city': 'Bellefonte',
			'state': 'PA',
			'zip': '16823',
			'delivery_instructions': 'Leave on porch',
		}
		form = UserAddressForm(data=data)
		self.assertTrue(form.is_valid())
		self.assertEqual(len(form.errors), 0)
	
	def test_field_length(self):
		self.assertEqual(len(self.form.fields), 9)


class TestPwdResetForm(TestCase):
	
	def setUp(self):
		self.form = PwdResetForm()
	
	def test_attrs(self):
		for field in self.form.fields:
			self.assertIn('class', self.form.fields[field].widget.attrs)
			self.assertIn('form-control', self.form.fields[field].widget.attrs['class'])
			self.assertIn('placeholder', self.form.fields[field].widget.attrs)
			self.assertIn('id', self.form.fields[field].widget.attrs)
			self.assertIn(f'form-{field}', self.form.fields[field].widget.attrs['id'])
	
	def test_form_is_valid(self):
		MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
		)
		data = {
			'email': 'email@email.com',
		}
		form = PwdResetForm(data=data)
		self.assertTrue(form.is_valid())
		self.assertEqual(len(form.errors), 0)
	
	def test_clean_email(self):
		data = {
			'email': 'email@email.com',
		}
		duplicate = PwdResetForm(data=data)
		self.assertFalse(duplicate.is_valid())
		self.assertEqual(duplicate["email"].errors, ['That email was not found. Please recheck the spelling.'])
	
	def test_field_length(self):
		self.assertEqual(len(self.form.fields), 1)


class TestSetPwdForm(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
		)
	
	def setUp(self):
		self.form = SetPwdForm(self.user)
	
	def test_attrs(self):
		for field in self.form.fields:
			self.assertIn('class', self.form.fields[field].widget.attrs)
			self.assertIn('form-control', self.form.fields[field].widget.attrs['class'])
			self.assertIn('placeholder', self.form.fields[field].widget.attrs)
			self.assertIn('id', self.form.fields[field].widget.attrs)
	
	def test_clean_new_password2(self):
		data = {
			'new_password1': 'GoodPassword111',
			'new_password2': 'GoodPassword222',
		}
		form = SetPwdForm(self.user, data=data)
		self.assertFalse(form.is_valid())
		self.assertEqual(form["new_password2"].errors, ['The two password fields didn’t match.'])
	
	def test_form_is_valid(self):
		data = {
			'new_password1': 'GoodPassword111',
			'new_password2': 'GoodPassword111',
		}
		form = SetPwdForm(self.user, data=data)
		self.assertTrue(form.is_valid())
		self.assertEqual(len(form.errors), 0)
	
	def test_field_length(self):
		self.assertEqual(len(self.form.fields), 2)


class TestPwdChangeForm(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
		)
	
	def setUp(self):
		self.form = PwdChangeForm(self.user)
	
	def test_attrs(self):
		for field in self.form.fields:
			self.assertIn('class', self.form.fields[field].widget.attrs)
			self.assertIn('form-control', self.form.fields[field].widget.attrs['class'])
			self.assertIn('placeholder', self.form.fields[field].widget.attrs)
			self.assertIn('id', self.form.fields[field].widget.attrs)
	
	def test_clean_new_password2(self):
		data = {
			'old_password': 'GoodPassword000',
			'new_password1': 'GoodPassword111',
			'new_password2': 'GoodPassword222',
		}
		form = PwdChangeForm(self.user, data=data)
		self.assertFalse(form.is_valid())
		self.assertEqual(form["new_password2"].errors, ['The two password fields didn’t match.'])
	
	def test_form_is_valid(self):
		data = {
			'old_password': 'GoodPassword000',
			'new_password1': 'GoodPassword111',
			'new_password2': 'GoodPassword111',
		}
		form = PwdChangeForm(self.user, data=data)
		self.assertTrue(form.is_valid())
		self.assertEqual(len(form.errors), 0)
	
	def test_field_length(self):
		self.assertEqual(len(self.form.fields), 3)
