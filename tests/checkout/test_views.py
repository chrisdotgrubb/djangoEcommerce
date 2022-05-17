from django.test import TestCase
from django.urls import reverse

from ecommerce.apps.checkout.models import DeliveryOptions
from ecommerce.apps.user.models import MyUser
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
	
	def test_purchase_in_session(self):
		pass
		# response = self.client.post(self.url)
		# context = response.context
		# self.assertIn('delivery_options', context)
		# self.assertIn('total', context)
		# self.assertIn('delivery_price', context)
		
	def test_login_required(self):
		self.client.logout()
		response = self.client.post(self.url)
		self.assertRedirects(response, f'{LOGIN_URL}?next={self.url}')
	
	def test_template_register(self):
		self.assertTemplateUsed(self.response, 'checkout/delivery_choices.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')
	
	