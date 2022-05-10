from django.test import TestCase
from django.urls import resolve, reverse
from ecommerce.apps.store import views


class TestUrls(TestCase):
	
	def setUp(self):
		pass
	
	def test_index_url(self):
		url = '/'
		rev_url = reverse('store:products_all')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.products_index_view)
	
	def test_product_detail_url(self):
		slug = 'slug'
		url = f'/{slug}/'
		rev_url = reverse('store:product_detail', args=[slug])
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.product_detail_view)
	
	def test_category_url(self):
		slug = 'slug'
		url = f'/shop/{slug}/'
		rev_url = reverse('store:category', args=[slug])
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.category_view)
