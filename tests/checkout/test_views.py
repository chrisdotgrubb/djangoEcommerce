from django.test import TestCase
from django.urls import reverse

from ecommerce.apps.checkout.models import DeliveryOptions
from ecommerce.apps.order.models import Order
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
	
	def test_template_choices(self):
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


class TestPaymentSelection(TestCase):
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
		self.url = reverse('checkout:payment_selection')
		
		session = self.client.session
		session['purchase'] = {}
		session['purchase']['delivery_id'] = self.delivery_option_1.pk
		session['address'] = {'address_id': str(self.address.pk)}
		session.save()
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_context(self):
		context = self.response.context
		self.assertIn('subtotal', context)
		self.assertIn('tax', context)
		self.assertIn('delivery_price', context)
		self.assertIn('total', context)
	
	def test_address_not_in_session(self):
		session = self.client.session
		del session['address']
		session.save()
		response = self.client.get(self.url, HTTP_REFERER=reverse('checkout:delivery_address'), follow=True)
		self.assertRedirects(response, reverse('checkout:delivery_address'))
		messages = list(response.context['messages'])
		self.assertEqual(str(messages[0]), 'Please select a delivery address.')
	
	def test_delivery_id_not_in_session(self):
		session = self.client.session
		del session['purchase']
		session.save()
		response = self.client.get(self.url, follow=True)
		self.assertRedirects(response, reverse('checkout:delivery_choices'))
		messages = list(response.context['messages'])
		self.assertEqual(str(messages[0]), 'Please select a different delivery option.')
	
	def test_login_required(self):
		self.client.logout()
		response = self.client.get(self.url)
		self.assertRedirects(response, f'{LOGIN_URL}?next={self.url}')
	
	def test_template_payment_selection(self):
		self.assertTemplateUsed(self.response, 'checkout/payment_selection.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')


class TestPaymentComplete(TestCase):
	pass


class TestPaymentSuccess(TestCase):
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
	first = 'first'
	address1 = '123 Main Street'
	address2 = 'Apt. 1'
	city = 'Bellefonte'
	zip_code = '16823'
	total_paid = 100
	order_key = 'key_from_PayPal'
	payment_option = 'PayPal'
	is_paid = True
	user_1 = None
	delivery_option = None
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
		)
		cls.delivery_option = DeliveryOptions.objects.create(
			delivery_method='PA',
			delivery_name='Ground Shipping',
			delivery_price=9.99,
			delivery_timeframe='3-5 Business Days',
			delivery_window='8-5',
			order=1
		)
		
		cls.order_1 = Order.objects.create(
			user=cls.user,
			name=cls.name,
			email=cls.email,
			address1=cls.address1,
			address2=cls.address2,
			city=cls.city,
			state=cls.state,
			country=cls.country,
			zip_code=cls.zip_code,
			delivery_instructions=cls.delivery_instructions,
			total_paid=cls.total_paid,
			order_key=cls.order_key,
			payment_option=cls.payment_option,
			delivery_option=cls.delivery_option,
			is_paid=cls.is_paid
		)
	
	def setUp(self):
		self.client.force_login(self.user)
		self.url = reverse('checkout:payment_success')
		
		session = self.client.session
		session['cart'] = {}
		session['cart'][1] = {'name': 'abc', 'qty': 1}
		session['cart'][2] = {'name': 'def', 'qty': 1}
		session['purchase'] = {'name': 'abc', 'qty': 1}
		session['address'] = {'name': 'abc', 'qty': 1}
		session.save()
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_context(self):
		context = self.response.context
		self.assertIn('order', context)
		self.assertEqual(context['order'], self.order_1)
	
	def test_cart_clear(self):
		session = self.client.session
		self.assertEqual(session['cart'], {})
		self.assertNotIn('purchase', session)
		self.assertNotIn('address', session)
	
	def test_no_order(self):
		self.order_1.delete()
		response = self.client.get(self.url)
		self.assertEqual(response.context['order'], None)
		messages = list(response.context['messages'])
		self.assertEqual(str(messages[0]), 'There was a problem with your order.')
	
	def test_order_not_paid(self):
		self.order_1.is_paid = False
		self.order_1.save()
		response = self.client.get(self.url)
		self.assertEqual(response.context['order'], None)
		messages = list(response.context['messages'])
		self.assertEqual(str(messages[0]), 'There was a problem with your order.')
	
	def test_login_required(self):
		self.client.logout()
		response = self.client.get(self.url)
		self.assertRedirects(response, f'{LOGIN_URL}?next={self.url}')
	
	def test_template_payment_success(self):
		self.assertTemplateUsed(self.response, 'checkout/payment_success.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')


class TestUpdateDelivery(TestCase):
	pass
