from django.test import TestCase
from store.models import Category, Product
from user.models import MyUser

class CategoryModelTest(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		cls.category = Category.objects.create(name='django', slug='django')
		
	def test_entry(self):
		self.assertTrue(isinstance(self.category, Category))
	
	def test_str(self):
		self.assertEqual(str(self.category), 'django')


class ProductModelTest(TestCase):
	
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
		
	def test_entry(self):
		self.assertTrue(isinstance(self.product, Product))
		
	def test_str(self):
		self.assertEqual(str(self.product), 'django beginners')

