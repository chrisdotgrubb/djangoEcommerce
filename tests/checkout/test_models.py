from django.test import TestCase
from ecommerce.apps.checkout.models import DeliveryOptions


class TestDeliveryOptions(TestCase):
	delivery_name_1 = 'Pick up'
	delivery_price_1 = 100
	delivery_method_1 = 'IS'
	delivery_timeframe_1 = 'Immediately'
	delivery_window_1 = '8-5'
	order_1 = 1
	
	@classmethod
	def setUpTestData(cls):
		cls.delivery_option_1 = DeliveryOptions.objects.create(
			delivery_name=cls.delivery_name_1,
			delivery_price=cls.delivery_price_1,
			delivery_method=cls.delivery_method_1,
			delivery_timeframe=cls.delivery_timeframe_1,
			delivery_window=cls.delivery_window_1,
			order=cls.order_1,
		)
	
	def test_str(self):
		self.assertEqual(str(self.delivery_option_1), self.delivery_name_1)
		
class TestPaymentSelections(TestCase):
	name_1 = 'name'
	
	@classmethod
	def setUpTestData(cls):
		pass
	
	
