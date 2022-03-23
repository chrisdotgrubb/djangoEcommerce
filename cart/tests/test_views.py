from django.test import TestCase
from django.urls import reverse
from store.models import Category, Product
from user.models import MyUser


#TODO  these tests need work, and add more
class CartViewTest(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.category = Category.objects.create(name='django', slug='django')
		cls.user = MyUser.objects.create(username='test')
		cls.product_1 = Product.objects.create(
			category_id=1,
			title='django beginners',
			created_by_id=1,
			slug='django-beginners',
			price='20.00',
			image='django.img'
		)
		cls.product_2 = Product.objects.create(
			category_id=1,
			title='django intermediate',
			created_by_id=1,
			slug='django-intermediate',
			price='20.00',
			image='django.img'
		)
		cls.product_3 = Product.objects.create(
			category_id=1,
			title='django advanced',
			created_by_id=1,
			slug='django-advanced',
			price='20.00',
			image='django.img'
		)
		
	def setUp(self):
		self.response = self.client.post(reverse('cart:add', kwargs={'product_id': 1,}), data={'qty': 10})
	
	def test_html(self):
		response = self.client.post(reverse('cart:add', kwargs={'product_id': 1,}), data={'qty': 10})
		html = response.content.decode('utf-8')
		self.assertTrue(html.startswith('<form hx-post="/cart/add/1/">'))
	
	
	