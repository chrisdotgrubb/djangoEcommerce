import logging

from django.test import TestCase
from django.urls import reverse, resolve
from ecommerce.apps.store import views


class UrlsTest(TestCase):
	
	def test_allowed_hosts(self):
		logging.debug('↓ ↓ ↓ EXPECTED ERROR and WARNING BETWEEN for testing not-allowed host ↓ ↓ ↓')
		response = self.client.get('/', HTTP_HOST='wrongaddress.com')
		logging.debug('↑ ↑ ↑ EXPECTED ERROR and WARNING BETWEEN for testing not-allowed host ↑ ↑ ↑')
		self.assertEqual(response.status_code, 400)
		response = self.client.get('/', HTTP_HOST='localhost')
		self.assertEqual(response.status_code, 200)
		
	def test_home_url(self):
		url = '/'
		rev_url = reverse('store:products_all')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.products_index_view)


