from django.test import TestCase
from django.urls import reverse, resolve
from store import views


class UrlsTest(TestCase):
	
	def test_allowed_hosts(self):
		response = self.client.get('/', HTTP_HOST='wrongaddress.com')
		self.assertEqual(response.status_code, 400)
		response = self.client.get('/', HTTP_HOST='localhost')
		self.assertEqual(response.status_code, 200)
		
	def test_home_url(self):
		url = '/'
		rev_url = reverse('store:products_all')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.products_all_view)


