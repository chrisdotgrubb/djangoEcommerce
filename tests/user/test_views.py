import re

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from ecommerce.apps.user.models import Address, MyUser


class TestUserRegistration(TestCase):
	
	def setUp(self):
		self.url = reverse('user:register')
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_post(self):
		data = {
			'email': 'email@email.com',
			'username': 'username',
			'password1': 'GoodPassword000',
			'password2': 'GoodPassword000'
		}
		users_before = len(MyUser.objects.all())
		response = self.client.post(self.url, data=data)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse('store:products_all'))
		users_after = len(MyUser.objects.all())
		self.assertEqual(users_after, users_before + 1)
	
	def test_is_logged_in(self):
		user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			password='GoodPassword000',
		)
		self.client.force_login(user)
		response = self.client.get(self.url)
		self.assertRedirects(response, reverse('store:products_all'))
	
	def test_template_register(self):
		self.assertTemplateUsed(self.response, 'registration/register.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')


class TestAccountActivate(TestCase):
	
	def setUp(self):
		url = reverse('user:register')
		data = {
			'email': 'email@email.com',
			'username': 'username',
			'password1': 'GoodPassword000',
			'password2': 'GoodPassword000'
		}
		self.client.post(url, data=data)
		
		regex = 'http://testserver/user/activate/(.*)/(.*)/'
		results = re.search(regex, mail.outbox[0].body)
		self.uidb64 = results.group(1)
		self.token = results.group(2)
	
	def test_activate_success(self):
		self.url = reverse('user:activate', args=[self.uidb64, self.token])
		self.response = self.client.get(self.url)
		self.assertRedirects(self.response, reverse('user:dashboard'))
		print(self.uidb64)
	
	def test_valid_but_wrong_uidb64(self):
		self.uidb64 = 'MzI4'
		self.url = reverse('user:activate', args=[self.uidb64, self.token])
		self.response = self.client.get(self.url)
		self.assertTemplateUsed('registration/activation_invalid.html')
	
	def test_invalid_uidb64(self):
		self.uidb64 = 'MzI4abc'
		self.url = reverse('user:activate', args=[self.uidb64, self.token])
		self.response = self.client.get(self.url)
		messages = list(self.response.context['messages'])
		self.assertEqual(str(messages[0]), 'Account created, check your email to confirm activation.')
		self.assertEqual(str(messages[1]), 'Account error, may have already been activated.')
		self.assertTemplateUsed('registration/activation_invalid.html')
	
	def test_bad_token(self):
		self.token = 'good_user_but_bad_token'
		self.url = reverse('user:activate', args=[self.uidb64, self.token])
		self.response = self.client.get(self.url)
		messages = list(self.response.context['messages'])
		self.assertEqual(str(messages[0]), 'Account created, check your email to confirm activation.')
		self.assertEqual(str(messages[1]), 'Account error, may have already been activated.')
		self.assertTemplateUsed('registration/activation_invalid.html')


class TestDashboard(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			password='GoodPassword000',
		)
	
	def setUp(self):
		self.client.force_login(self.user)
		self.url = reverse('user:dashboard')
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_login_required(self):
		self.client.logout()
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 302)
	
	def test_template_dashboard(self):
		self.assertTemplateUsed(self.response, 'user/dashboard.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')


class TestEditProfile(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
		)
	
	def setUp(self):
		self.client.force_login(self.user)
		self.url = reverse('user:edit_profile')
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.context['form'].instance, self.user)
		self.assertEqual(self.response.status_code, 200)
	
	def test_post(self):
		data = {
			'username': self.user.username,
			'email': self.user.email,
			'first': 'changed',
			'phone': '(814)574-0000'
			
		}
		response = self.client.post(self.url, data=data)
		user = MyUser.objects.all()[0]
		self.assertEqual(user.username, 'username')
		self.assertEqual(user.email, 'email@email.com')
		self.assertEqual(user.first, 'changed')
		self.assertEqual(user.phone, '(814)574-0000')
		
		self.assertEqual(response.status_code, 200)
		messages = list(response.context['messages'])
		self.assertEqual(str(messages[0]), 'Profile updated.')
	
	def test_form_invalid(self):
		data = {
			'username': self.user.username,
			'email': self.user.email,
			'first': 'changed',
			'phone': '123'
			
		}
		response = self.client.post(self.url, data=data, follow=True)
		user = MyUser.objects.all()[0]
		self.assertEqual(user.username, 'username')
		self.assertEqual(user.email, 'email@email.com')
		self.assertEqual(user.first, 'first name')
		
		self.assertEqual(response.status_code, 200)
		messages = list(response.context['messages'])
		self.assertEqual(str(messages[0]), 'Profile update failed.')
	
	def test_template_edit_profile(self):
		self.assertTemplateUsed(self.response, 'user/edit_profile.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')


class TestDeleteProfile(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
		)
		
	def setUp(self):
		self.client.force_login(self.user)
		self.url = reverse('user:delete_profile')
	
	def test_delete(self):
		active_before = len(MyUser.active.all())
		inactive_before = len(MyUser.inactive.all())
		total_before = len(MyUser.objects.all())
		self.assertEqual(self.user.is_active, True)
		
		response = self.client.get(self.url)
		
		active_after = len(MyUser.active.all())
		inactive_after = len(MyUser.inactive.all())
		total_after = len(MyUser.objects.all())
		self.assertEqual(active_before - 1, active_after)
		self.assertEqual(inactive_before + 1, inactive_after)
		self.assertEqual(total_before, total_after)
		
		user = MyUser.objects.get(username='username')
		self.assertEqual(user.is_active, False)
		self.assertRedirects(response, reverse('user:delete_finished'))


class TestCheckUsername(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
		)
		cls.deleted = MyUser.objects.create_superuser(
			email='deleted@email.com',
			username='deleted',
			first='first name',
			password='GoodPassword000',
			is_active=False
		)
		
	def setUp(self):
		self.url = reverse('user:check_username')
	
	def test_good(self):
		self.response = self.client.post(self.url, data={'username': 'available'})
		self.assertEqual(self.response.status_code, 200)
		self.assertTrue('Username available' in str(self.response.content))
	
	def test_short(self):
		self.response = self.client.post(self.url, data={'username': '123'})
		self.assertEqual(self.response.status_code, 200)
		self.assertTrue('Username too short' in str(self.response.content))
	
	def test_taken(self):
		self.response = self.client.post(self.url, data={'username': 'username'})
		self.assertEqual(self.response.status_code, 200)
		self.assertTrue('Username taken' in str(self.response.content))
	
	def test_inactive(self):
		self.response = self.client.post(self.url, data={'username': 'deleted'})
		self.assertEqual(self.response.status_code, 200)
		self.assertTrue('username may have been recently deleted' in str(self.response.content))
	
	def test_else(self):
		self.response = self.client.post(self.url, data={'username': ''})
		self.assertEqual(self.response.status_code, 200)
		self.assertTrue('&nbsp' in str(self.response.content))


class TestCheckEmail(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
		)
		cls.deleted = MyUser.objects.create_superuser(
			email='deleted@email.com',
			username='deleted',
			first='first name',
			password='GoodPassword000',
			is_active=False
		)
	
	def setUp(self):
		self.url = reverse('user:check_email')
	
	def test_good(self):
		self.response = self.client.post(self.url, data={'email': 'available@email.com'})
		self.assertEqual(self.response.status_code, 200)
		self.assertTrue('Email available' in str(self.response.content))
	
	def test_taken(self):
		self.response = self.client.post(self.url, data={'email': 'email@email.com'})
		self.assertEqual(self.response.status_code, 200)
		self.assertTrue('Email taken' in str(self.response.content))
	
	def test_inactive(self):
		self.response = self.client.post(self.url, data={'email': 'deleted@email.com'})
		self.assertEqual(self.response.status_code, 200)
		self.assertTrue('email may have been recently deleted' in str(self.response.content))
	
	def test_else(self):
		self.response = self.client.post(self.url, data={'email': ''})
		self.assertEqual(self.response.status_code, 200)
		self.assertTrue('&nbsp' in str(self.response.content))
	
	def test_regex_good(self):
		response = self.client.post(self.url, data={'email': 'TEST@EMAIL.COM'})
		self.assertTrue('Email available' in str(response.content))
		
		response = self.client.post(self.url, data={'email': 'first.last@test.com'})
		self.assertTrue('Email available' in str(response.content))
		
		response = self.client.post(self.url, data={'email': 'first-last@test.co.uk'})
		self.assertTrue('Email available' in str(response.content))
		
		response = self.client.post(self.url, data={'email': 'first_last@test.com'})
		self.assertTrue('Email available' in str(response.content))
	
	def test_regex_bad(self):
		response = self.client.post(self.url, data={'email': 'email'})
		self.assertTrue('Email not valid' in str(response.content))
		
		response = self.client.post(self.url, data={'email': 'test@test.com.'})
		self.assertTrue('Email not valid' in str(response.content))
		
		response = self.client.post(self.url, data={'email': 'test@test.c'})
		self.assertTrue('Email not valid' in str(response.content))
		
		response = self.client.post(self.url, data={'email': '@test.com'})
		self.assertTrue('Email not valid' in str(response.content))
		
		response = self.client.post(self.url, data={'email': '"test"@test.com'})
		self.assertTrue('Email not valid' in str(response.content))


class TestAddressList(TestCase):
	user = None
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
		)
		cls.address_1 = Address.objects.create(
			customer=cls.user,
			name='one',
			phone='(814)574-0000',
			country='US',
			address_line_1='123 Main Street',
			address_line_2='Apartment 2',
			town_city='Bellefonte',
			state='PA',
			zip='16823',
			delivery_instructions='Leave on porch',
		)
		cls.address_2 = Address.objects.create(
			customer=cls.user,
			name='two',
			phone='(814)574-0001',
			country='US',
			address_line_1='124 Main Street',
			address_line_2='Apartment 1',
			town_city='Bellefonte',
			state='PA',
			zip='16823',
			delivery_instructions='Leave at back',
		)
		
	def setUp(self):
		self.client.force_login(self.user)
		self.url = reverse('user:addresses')
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_login_required(self):
		self.client.logout()
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 302)
	
	def test_context(self):
		context = self.response.context['addresses']
		self.assertEqual(len(context), 2)
	
	def test_template_address_list(self):
		self.assertTemplateUsed(self.response, 'user/address/list.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')


class TestAddressForm(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
		)
	
	def setUp(self):
		self.client.force_login(self.user)
		self.url = reverse('user:address_form')
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_context(self):
		self.assertIn('form', self.response.context)
	
	def test_login_required(self):
		self.client.logout()
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 302)
		
	def test_template_address_form(self):
		self.assertTemplateUsed(self.response, 'user/address/_address_form.html')


class TestGetAddress(TestCase):
	user = None
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
		)
		cls.address_1 = Address.objects.create(
			customer=cls.user,
			name='Test name',
			phone='(814)574-0000',
			country='US',
			address_line_1='123 Main Street',
			address_line_2='Apartment 2',
			town_city='Bellefonte',
			state='PA',
			zip='16823',
			delivery_instructions='Leave on porch',
		)
		
	def setUp(self):
		
		self.client.force_login(self.user)
		self.url = reverse('user:get_address', args=[self.address_1.pk])
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_context(self):
		context = self.response.context['address']
		self.assertEqual(self.address_1, context)
	
	def test_htmx_trigger(self):
		self.assertIn('addressAddedEvent', self.response.headers['hx-trigger'])
		
	def test_login_required(self):
		self.client.logout()
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 302)
	
	def test_template_address_form(self):
		self.assertTemplateUsed(self.response, 'user/address/_address.html')


class TestAddAddress(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
		)
		cls.data = {
			'name': 'name',
			'phone': '(814) 574-0000',
			'address_line_1': '123 Main Street',
			'address_line_2': 'Apartment 2',
			'town_city': 'Bellefonte',
			'state': 'PA',
			'zip': '16823',
			'country': 'US',
			'delivery_instructions': 'Leave on porch',
		}
		
	def setUp(self):
		self.client.force_login(self.user)
		self.url = reverse('user:add_address')
		self.response = self.client.post(self.url, data=self.data)
	
	def test_post(self):
		address = Address.objects.get(customer=self.user, name='name')
		self.assertRedirects(self.response, reverse('user:get_address', args=[address.pk]))
	
	def test_login_required(self):
		self.client.logout()
		response = self.client.post(self.url)
		self.assertRedirects(response, '/user/login/?next=/user/add_address/')
	
	def test_post_required(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 405)
		

class TestNewAddressBtn(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
		)
		
	def setUp(self):
		self.client.force_login(self.user)
		self.url = reverse('user:new_address_btn')
		self.response = self.client.get(self.url)
		
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_login_required(self):
		self.client.logout()
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 302)
	
	def test_template_new_address_btn(self):
		self.assertTemplateUsed(self.response, 'user/address/_new_address_btn.html')
	
	
	