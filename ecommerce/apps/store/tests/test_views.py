from importlib import import_module
from django.conf import settings
from django.http import HttpRequest
from django.test import TestCase, RequestFactory
from django.urls import reverse
from ecommerce.apps.store.models import Category, Product
from ecommerce.apps.user.models import MyUser
from ecommerce.apps.store import views

class ProductsAllViewTest(TestCase):
	
	def setUp(self):
		self.url = reverse('store:products_all')
		self.request = RequestFactory().get(self.url)
		self.request.session = import_module(settings.SESSION_ENGINE).SessionStore()
		self.response = views.products_index_view(self.request).render()
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_html(self):
		request = HttpRequest()
		request.session = import_module(settings.SESSION_ENGINE).SessionStore()
		response = views.products_index_view(request)
		rendered = response.render()
		html = rendered.content.decode('utf-8')
		self.assertIn('<title>Book Store</title>', html)
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
		self.request = RequestFactory().get(self.url)
		self.request.session = import_module(settings.SESSION_ENGINE).SessionStore()
		self.response = views.product_detail_view(self.request, slug='django-beginners').render()
		
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
