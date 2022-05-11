from django.test import TestCase
from django.urls import resolve, reverse

from ecommerce.apps.checkout import views


class TestUrls(TestCase):
	
	def setUp(self):
		pass
	
	def test_delivery_choices(self):
		url = '/checkout/delivery_choices/'
		rev_url = reverse('checkout:delivery_choices')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.delivery_choices_view)
	
	def test_delivery_address(self):
		url = '/checkout/delivery_address/'
		rev_url = reverse('checkout:delivery_address')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.delivery_address_view)
	
	def test_payment_selection(self):
		url = '/checkout/payment_selection/'
		rev_url = reverse('checkout:payment_selection')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.payment_selection_view)
	
	def test_payment_complete(self):
		url = '/checkout/payment_complete/'
		rev_url = reverse('checkout:payment_complete')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.payment_complete_view)
	
	def test_payment_success(self):
		url = '/checkout/payment_success/'
		rev_url = reverse('checkout:payment_success')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.payment_success_view)
	
	def test_update_delivery(self):
		pk = 1
		url = f'/checkout/update_delivery/{pk}/'
		rev_url = reverse('checkout:update_delivery', args=[pk])
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.update_delivery)
	
