from django.test import TestCase
from django.urls import reverse

from ecommerce.apps.checkout.models import DeliveryOptions
from ecommerce.apps.user.models import Address, MyUser
from ecommerce.settings.base import LOGIN_URL


class TestDeliveryChoices(TestCase):
	delivery_name_1 = 'Ground'
	delivery_price_1 = 5.99
	delivery_method_1 = 'PA'
	delivery_timeframe_1 = '3-5 days'
	delivery_window_1 = '8am-8pm'
	order_1 = 0
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
		)
		
		cls.delivery_option_1 = DeliveryOptions.objects.create(
			delivery_name=cls.delivery_name_1,
			delivery_price=cls.delivery_price_1,
			delivery_method=cls.delivery_method_1,
			delivery_timeframe=cls.delivery_timeframe_1,
			delivery_window=cls.delivery_window_1,
			order=cls.order_1,
		)
	
	def setUp(self):
		self.client.force_login(self.user)
		self.url = reverse('checkout:delivery_choices')
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
		
	def test_context(self):
		context = self.response.context
		self.assertIn('delivery_options', context)
	
	def test_delivery_option_in_session(self):
		session = self.client.session
		session['purchase'] = {}
		session['purchase']['delivery_id'] = self.delivery_option_1.pk
		session.save()
		response = self.client.get(self.url)
		context = response.context
		self.assertIn('total', context)
		self.assertIn('delivery_price', context)
		
	def test_delivery_option_empty(self):
		session = self.client.session
		session['purchase'] = {}
		session['purchase']['delivery_id'] = None
		session.save()
		response = self.client.get(self.url)
		context = response.context
		self.assertNotIn('total', context)
		self.assertNotIn('delivery_price', context)
		
	def test_delivery_option_wrong(self):
		session = self.client.session
		session['purchase'] = {}
		session['purchase']['delivery_id'] = 999
		session.save()
		response = self.client.get(self.url)
		context = response.context
		self.assertNotIn('total', context)
		self.assertNotIn('delivery_price', context)
		
	def test_login_required(self):
		self.client.logout()
		response = self.client.get(self.url)
		self.assertRedirects(response, f'{LOGIN_URL}?next={self.url}')
	
	def test_template_register(self):
		self.assertTemplateUsed(self.response, 'checkout/delivery_choices.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')


class TestDeliveryAddress(TestCase):
	delivery_name_1 = 'Ground'
	delivery_price_1 = 5.99
	delivery_method_1 = 'PA'
	delivery_timeframe_1 = '3-5 days'
	delivery_window_1 = '8am-8pm'
	order_1 = 0
	email = 'test@test.com'
	username = 'test'
	password = 'password'
	name = 'name'
	phone = '814-574-0000'
	country = 'US'
	address_line_1 = '123 Main Street.'
	address_line_2 = 'Apartment 3'
	town_city = 'Bellefonte'
	state = 'PA'
	zip = '16823'
	delivery_instructions = 'Leave on porch'
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
		
		cls.address = Address.objects.create(
			customer=cls.user,
			name=cls.name,
			phone=cls.phone,
			country=cls.country,
			address_line_1=cls.address_line_1,
			address_line_2=cls.address_line_2,
			town_city=cls.town_city,
			state=cls.state,
			zip=cls.zip,
			delivery_instructions=cls.delivery_instructions,
		)
		
		cls.delivery_option_1 = DeliveryOptions.objects.create(
			delivery_name=cls.delivery_name_1,
			delivery_price=cls.delivery_price_1,
			delivery_method=cls.delivery_method_1,
			delivery_timeframe=cls.delivery_timeframe_1,
			delivery_window=cls.delivery_window_1,
			order=cls.order_1,
		)
	
	def setUp(self):
		self.client.force_login(self.user)
		self.url = reverse('checkout:delivery_address')
		
		session = self.client.session
		session['purchase'] = {}
		session['purchase']['delivery_id'] = self.delivery_option_1.pk
		session.save()
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_context(self):
		context = self.response.context
		self.assertIn('addresses', context)
		self.assertIn('subtotal', context)
		self.assertIn('tax', context)
		self.assertIn('delivery_price', context)
		self.assertIn('total', context)
		self.assertIn('has_default', context)
	
	def test_purchase_not_in_session(self):
		session = self.client.session
		del session['purchase']
		session.save()
		response = self.client.get(self.url, HTTP_REFERER=reverse('checkout:delivery_choices'), follow=True)
		self.assertRedirects(response, reverse('checkout:delivery_choices'))
		messages = list(response.context['messages'])
		self.assertEqual(str(messages[0]), 'Please select a delivery option.')
		
	def test_delivery_option_inactive(self):
		self.delivery_option_1.is_active = False
		self.delivery_option_1.save()
		session = self.client.session
		session['purchase'] = {}
		session['purchase']['delivery_id'] = self.delivery_option_1.pk
		session.save()
		response = self.client.get(self.url, HTTP_REFERER=reverse('checkout:delivery_choices'), follow=True)
		self.assertRedirects(response, reverse('checkout:delivery_choices'))
		messages = list(response.context['messages'])
		self.assertEqual(str(messages[0]), 'Please select a different delivery option.')
		
	def test_delivery_option_wrong(self):
		session = self.client.session
		session['purchase'] = {}
		session['purchase']['delivery_id'] = 999
		session.save()
		response = self.client.get(self.url, HTTP_REFERER=reverse('checkout:delivery_choices'), follow=True)
		self.assertRedirects(response, reverse('checkout:delivery_choices'))
		messages = list(response.context['messages'])
		self.assertEqual(str(messages[0]), 'Please select a different delivery option.')
	
	def test_default_address(self):
		self.address.default = True
		self.address.save()
		response = self.client.get(self.url)
		context = response.context
		self.assertEqual(context['has_default'], True)
		
		self.address.default = False
		self.address.save()
		response = self.client.get(self.url)
		context = response.context
		self.assertEqual(context['has_default'], False)
	
	def test_no_address(self):
		self.address.delete()
		response = self.client.get(self.url, follow=True)
		self.assertRedirects(response, reverse('user:addresses'))
		messages = list(response.context['messages'])
		self.assertEqual(str(messages[0]), 'Please add an address for delivery, then checkout again.')
		
	def test_login_required(self):
		self.client.logout()
		response = self.client.get(self.url)
		self.assertRedirects(response, f'{LOGIN_URL}?next={self.url}')
	
	def test_template_register(self):
		self.assertTemplateUsed(self.response, 'checkout/delivery_address.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')
	
	