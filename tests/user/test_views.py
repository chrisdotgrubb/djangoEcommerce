import re

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from ecommerce.apps.checkout.models import DeliveryOptions
from ecommerce.apps.order.models import Order
from ecommerce.apps.store.models import Category, Product, ProductType
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
		user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			password='GoodPassword000',
			is_active=True
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
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			password='GoodPassword000',
			is_active=True
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
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
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
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
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
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
		)
		cls.deleted = MyUser.objects.create_user(
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
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
		)
		cls.deleted = MyUser.objects.create_user(
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
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
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
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
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
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
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
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
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
	
	def test_http_methods(self):
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 405)


class TestNewAddressBtn(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
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


class TestEditAddress(TestCase):
	user = None
	name = 'new name'
	phone = '(814) 574-0001'
	country = 'US'
	address_line_1 = 'new address'
	address_line_2 = 'new address ln 2'
	town_city = 'New York'
	state = 'NY'
	zip = '10001'
	delivery_instructions = 'new delivery instructions'
	data = {
		'name': name,
		'phone': phone,
		'country': country,
		'address_line_1': address_line_1,
		'address_line_2': address_line_2,
		'town_city': town_city,
		'state': state,
		'zip': zip,
		'delivery_instructions': delivery_instructions,
	}
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
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
		self.uuid = self.address_1.pk
		self.url = reverse('user:edit_address', args=[self.uuid])
	
	def test_get(self):
		response = self.client.get(self.url)
		self.assertEqual(response.context['form'].initial['name'], 'Test name')
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'user/address/edit.html')
	
	def test_post(self):
		response = self.client.post(self.url, data=self.data)
		self.assertRedirects(response, reverse('user:addresses'))
	
	def test_form_invalid(self):
		data = {
			'name': self.name,
			'phone': '123',
			'country': self.country,
			'address_line_1': self.address_line_1,
			'address_line_2': self.address_line_2,
			'town_city': self.town_city,
			'state': self.state,
			'zip': self.zip,
			'delivery_instructions': self.delivery_instructions,
		}
		response = self.client.post(self.url, data=data)
		self.assertRedirects(response, '/')
	
	def test_login_required(self):
		self.client.logout()
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 302)


class TestDeleteAddress(TestCase):
	user = None
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
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
		self.url = reverse('user:delete_address', args=[self.address_1.pk])
	
	def test_delete(self):
		before = len(Address.objects.all())
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.content, b'')
		after = len(Address.objects.all())
		self.assertEqual(before - 1, after)
	
	def test_login_required(self):
		self.client.logout()
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 302)


class TestSetDefaultAddress(TestCase):
	user = None
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
		)
		cls.address_1 = Address.objects.create(
			customer=cls.user,
			name='First',
			phone='(814)574-0000',
			country='US',
			address_line_1='123 Main Street',
			address_line_2='Apartment 1',
			town_city='Bellefonte',
			state='PA',
			zip='16823',
			delivery_instructions='Leave on porch',
		)
		cls.address_2 = Address.objects.create(
			customer=cls.user,
			name='Second',
			phone='(814)574-0001',
			country='US',
			address_line_1='124 Main Street',
			address_line_2='Apartment 2',
			town_city='Bellefonte',
			state='PA',
			zip='16823',
			delivery_instructions='Leave at back',
		)
		cls.address_3 = Address.objects.create(
			customer=cls.user,
			name='Third',
			phone='(814)574-0002',
			country='US',
			address_line_1='125 Main Street',
			address_line_2='Apartment 3',
			town_city='Bellefonte',
			state='PA',
			zip='16823',
			delivery_instructions='Leave at back',
		)
	
	def setUp(self):
		self.client.force_login(self.user)
		self.url = reverse('user:set_default_address', args=[self.address_1.pk])
	
	def test_set_default(self):
		dash = reverse('user:dashboard')
		url = reverse('user:set_default_address', args=[self.address_1.pk])
		response = self.client.get(url, HTTP_REFERER=dash)
		self.assertRedirects(response, dash)
		self.assertEqual(Address.objects.get(name='First'), Address.objects.get(default=True))
		self.assertEqual(len(Address.objects.filter(default=False)), 2)
		
		url = reverse('user:set_default_address', args=[self.address_2.pk])
		response = self.client.get(url, HTTP_REFERER=dash)
		self.assertRedirects(response, dash)
		self.assertEqual(Address.objects.get(name='Second'), Address.objects.get(default=True))
		self.assertEqual(len(Address.objects.filter(default=False)), 2)
		
		url = reverse('user:set_default_address', args=[self.address_3.pk])
		response = self.client.get(url, HTTP_REFERER=dash)
		self.assertRedirects(response, dash)
		self.assertEqual(Address.objects.get(name='Third'), Address.objects.get(default=True))
		self.assertEqual(len(Address.objects.filter(default=False)), 2)
	
	def test_login_required(self):
		self.client.logout()
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 302)


class TestAddToWishlist(TestCase):
	category_name_1 = 'category'
	type_name_1 = 'type'
	title_1 = 'product 1'
	title_2 = 'product 1'
	description_1 = 'description 1'
	description_2 = 'description 2'
	regular_price_1 = 25
	regular_price_2 = 25
	discount_price_1 = 20
	discount_price_2 = 20
	type_1 = None
	category_1 = None
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
		)
		
		cls.category_1 = Category.objects.create(name=cls.category_name_1)
		cls.type_1 = ProductType.objects.create(name=cls.type_name_1)
		
		cls.product_1 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_1,
			title=cls.title_1,
			description=cls.description_1,
			regular_price=cls.regular_price_1,
			discount_price=cls.discount_price_1
		)
		
		cls.product_2 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_1,
			title=cls.title_2,
			description=cls.description_2,
			regular_price=cls.regular_price_2,
			discount_price=cls.discount_price_2
		)
	
	def setUp(self):
		self.client.force_login(user=self.user)
	
	def test_add_delete_wishlist_items(self):
		dash = reverse('user:dashboard')
		
		# check that product 1 is not in wishlist, and wishlist empty
		self.assertFalse(self.product_1.users_wishlist.filter(id=self.user.pk).exists())
		self.assertEqual(len(self.user.user_wishlist.all()), 0)
		
		# add product 1 and check that it is added
		url = reverse('user:add_to_wishlist', args=[self.product_1.pk])
		response = self.client.get(url, HTTP_REFERER=dash)
		self.assertRedirects(response, dash)
		self.assertTrue(self.product_1.users_wishlist.filter(id=self.user.pk).exists())
		
		# remove product 1 and make sure it is gone
		response = self.client.get(url, HTTP_REFERER=dash)
		self.assertRedirects(response, dash)
		self.assertFalse(self.product_1.users_wishlist.filter(id=self.user.pk).exists())
		
		# add product 1 and 2 and check user's wishlist has 2 items
		response = self.client.get(url, HTTP_REFERER=dash)
		self.assertRedirects(response, dash)
		url = reverse('user:add_to_wishlist', args=[self.product_2.pk])
		response = self.client.get(url, HTTP_REFERER=dash)
		self.assertRedirects(response, dash)
		self.assertEqual(len(self.user.user_wishlist.all()), 2)
	
	def test_wishlist_messages(self):
		dash = reverse('user:dashboard')
		
		self.assertFalse(self.product_1.users_wishlist.filter(id=self.user.pk).exists())
		self.assertEqual(len(self.user.user_wishlist.all()), 0)
		
		url = reverse('user:add_to_wishlist', args=[self.product_1.pk])
		response = self.client.get(url, HTTP_REFERER=dash, follow=True)
		messages = list(response.context['messages'])
		self.assertEqual(str(messages[0]), f'Added {self.product_1.title} to your wishlist.')
		
		url = reverse('user:add_to_wishlist', args=[self.product_1.pk])
		response = self.client.get(url, HTTP_REFERER=dash, follow=True)
		messages = list(response.context['messages'])
		self.assertEqual(str(messages[0]), f'Removed {self.product_1.title} from your wishlist.')
	
	def test_404(self):
		self.assertFalse(Product.objects.filter(pk=100).exists())
		url = reverse('user:add_to_wishlist', args=[100])
		response = self.client.get(url, HTTP_REFERER=reverse('user:dashboard'))
		self.assertEqual(response.status_code, 404)
	
	def test_login_required(self):
		self.client.logout()
		url = reverse('user:add_to_wishlist', args=[self.product_1.pk])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 302)


class TestWishlist(TestCase):
	category_name_1 = 'category'
	type_name_1 = 'type'
	title_1 = 'product 1'
	title_2 = 'product 1'
	description_1 = 'description 1'
	description_2 = 'description 2'
	regular_price_1 = 25
	regular_price_2 = 25
	discount_price_1 = 20
	discount_price_2 = 20
	type_1 = None
	category_1 = None
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
		)
		
		cls.category_1 = Category.objects.create(name=cls.category_name_1)
		cls.type_1 = ProductType.objects.create(name=cls.type_name_1)
		
		cls.product_1 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_1,
			title=cls.title_1,
			description=cls.description_1,
			regular_price=cls.regular_price_1,
			discount_price=cls.discount_price_1
		)
		
		cls.product_2 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_1,
			title=cls.title_2,
			description=cls.description_2,
			regular_price=cls.regular_price_2,
			discount_price=cls.discount_price_2
		)
	
	def setUp(self):
		self.client.force_login(user=self.user)
		self.url = reverse('user:wishlist')
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_context(self):
		response = self.client.get(self.url)
		self.assertEqual(len(response.context['wishlist']), 0)
		
		self.product_1.users_wishlist.add(self.user)
		self.product_2.users_wishlist.add(self.user)
		
		response = self.client.get(self.url)
		self.assertEqual(len(response.context['wishlist']), 2)
		
		self.product_2.users_wishlist.remove(self.user)
		
		response = self.client.get(self.url)
		self.assertEqual(len(response.context['wishlist']), 1)
	
	def test_login_required(self):
		self.client.logout()
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 302)
	
	def test_template_address_list(self):
		self.assertTemplateUsed(self.response, 'user/user_wish_list.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')


class TestOrders(TestCase):
	email_1 = 'user_1@user.com'
	username_1 = 'user_1'
	password_1 = 'password'
	first_1 = 'first'
	name_1 = 'first last'
	address1_1 = '123 Main Street'
	address2_1 = 'Apt. 1'
	city_1 = 'Bellefonte'
	state_1 = 'PA'
	country_1 = 'US'
	zip_code_1 = '16823'
	delivery_instructions_1 = 'Front Door'
	total_paid_1 = 100
	order_key_1 = 'key_from_PayPal'
	payment_option_1 = 'PayPal'
	is_paid = True
	user = None
	delivery_option_1 = None
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_user(cls.email_1, cls.username_1, cls.password_1, is_active=True)
		
		cls.delivery_option_1 = DeliveryOptions.objects.create(
			delivery_method='PA',
			delivery_name='Ground Shipping',
			delivery_price=9.99,
			delivery_timeframe='3-5 Business Days',
			delivery_window='8-5',
			order=1
		)
		
		cls.order_1 = Order.objects.create(
			user=cls.user,
			name=cls.name_1,
			email=cls.email_1,
			address1=cls.address1_1,
			address2=cls.address2_1,
			city=cls.city_1,
			state=cls.state_1,
			country=cls.country_1,
			zip_code=cls.zip_code_1,
			delivery_instructions=cls.delivery_instructions_1,
			total_paid=cls.total_paid_1,
			order_key=cls.order_key_1,
			payment_option=cls.payment_option_1,
			delivery_option=cls.delivery_option_1,
			is_paid=cls.is_paid
		)
	
	def setUp(self):
		self.client.force_login(user=self.user)
		self.url = reverse('user:orders')
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_login_required(self):
		self.client.logout()
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 302)
	
	def test_template_address_list(self):
		self.assertTemplateUsed(self.response, 'user/orders.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')
