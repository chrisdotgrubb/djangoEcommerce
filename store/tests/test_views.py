from django.http import HttpRequest
from django.test import TestCase, RequestFactory
from django.urls import reverse
from store.models import Category, Product
from user.models import MyUser
from store import views

class AllProductsViewTest(TestCase):
	
	def setUp(self):
		self.url = reverse('store:all_products')
		self.response = self.client.get(self.url)
		
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
		
	def test_html(self):
		request = HttpRequest()
		response = views.all_products_view(request)
		rendered = response.render()
		html = rendered.content.decode('utf-8')
		self.assertIn('<title>Store</title>', html)
		self.assertTrue(html.startswith('\n<!DOCTYPE html>\n'))


class ProductDetailViewTest(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.category = Category.objects.create(name='django', slug='django')
		cls.user = MyUser.objects.create(username='test')
		cls.product = Product.objects.create(
			category_id=1,
			title='django beginners',
			created_by_id=1,
			slug='django-beginners',
			price='20.00',
			image='django.img'
		)
	
	def setUp(self):
		self.url = reverse('store:product_detail', args=['django-beginners'])
		self.response = self.client.get(self.url)
		
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)


class CategoryViewTest(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.category = Category.objects.create(name='django', slug='django')
	
	def setUp(self):
		self.url = reverse('store:category', args=['django'])
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)

