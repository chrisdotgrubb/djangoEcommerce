from django.test import TestCase
from django.urls import reverse

from ecommerce.apps.store.models import Category, Product, ProductType
from ecommerce.apps.user.models import MyUser


class TestProductsIndex(TestCase):
	category_name_1 = 'category'
	type_name_1 = 'type'
	title_1 = 'product 1'
	title_2 = 'product 2'
	title_3 = 'product 3'
	description_1 = 'description 1'
	description_2 = 'description 2'
	description_3 = 'description 3'
	regular_price_1 = 25
	regular_price_2 = 25
	regular_price_3 = 25
	discount_price_1 = 20
	discount_price_2 = 20
	discount_price_3 = 20
	type_1 = None
	category_1 = None
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
		)
		
		cls.category_1 = Category.objects.create(name=cls.category_name_1)
		cls.type_1 = ProductType.objects.create(name=cls.type_name_1)
		
		cls.product_1 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_1,
			title=cls.title_1,
			description=cls.description_1,
			regular_price=cls.regular_price_1,
			discount_price=cls.discount_price_1
		)
		
		cls.product_2 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_1,
			title=cls.title_2,
			description=cls.description_2,
			regular_price=cls.regular_price_2,
			discount_price=cls.discount_price_2
		)
		
		cls.product_3 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_1,
			title=cls.title_3,
			description=cls.description_3,
			regular_price=cls.regular_price_3,
			discount_price=cls.discount_price_3,
			is_active=False
		)
		
	def setUp(self):
		self.url = reverse('store:products_all')
		self.response = self.client.get(self.url)
		
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_products(self):
		self.assertEqual(len(self.response.context['products']), 2)
	
	def test_template_register(self):
		self.assertTemplateUsed(self.response, 'store/index.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')


class TestProductDetail(TestCase):
	category_name_1 = 'category'
	type_name_1 = 'type'
	title_1 = 'product 1'
	title_2 = 'product 2'
	description_1 = 'description 1'
	description_2 = 'description 2'
	regular_price_1 = 25
	regular_price_2 = 25
	discount_price_1 = 20
	discount_price_2 = 20
	type_1 = None
	category_1 = None
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
		)
		
		cls.category_1 = Category.objects.create(name=cls.category_name_1)
		cls.type_1 = ProductType.objects.create(name=cls.type_name_1)
		
		cls.product_1 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_1,
			title=cls.title_1,
			description=cls.description_1,
			regular_price=cls.regular_price_1,
			discount_price=cls.discount_price_1
		)
		
		cls.product_2 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_1,
			title=cls.title_2,
			description=cls.description_2,
			regular_price=cls.regular_price_2,
			discount_price=cls.discount_price_2,
			is_active=False
		)
		
	def setUp(self):
		self.url = reverse('store:product_detail', args=[self.product_1.slug])
		self.response = self.client.get(self.url)

	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
		
	def test_context(self):
		context = self.response.context
		self.assertIn('product', context)
		self.assertIn('form', context)
		self.assertIn('in_wish', context)
		
	def test_in_wish(self):
		self.client.force_login(self.user)
		self.assertEqual(self.response.context['in_wish'], False)
		
		self.product_1.users_wishlist.add(self.user)
		response = self.client.get(self.url)
		self.assertEqual(response.context['in_wish'], True)
		
		self.product_1.users_wishlist.remove(self.user)
		response = self.client.get(self.url)
		self.assertEqual(response.context['in_wish'], False)
	
	def test_404(self):
		inactive = reverse('store:product_detail', args=[self.product_2.slug])
		response = self.client.get(inactive)
		self.assertEqual(response.status_code, 404)
		
		wrong = reverse('store:product_detail', args=['does-not-exist'])
		response = self.client.get(wrong)
		self.assertEqual(response.status_code, 404)
	
	def test_template_register(self):
		self.assertTemplateUsed(self.response, 'store/product_detail.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')
		
		
class TestCategory(TestCase):
	category_name_1 = 'category'
	category_name_2 = 'category 2'
	type_name_1 = 'type'
	title_1 = 'product 1'
	title_2 = 'product 2'
	title_3 = 'product 3'
	description_1 = 'description 1'
	description_2 = 'description 2'
	description_3 = 'description 3'
	regular_price_1 = 25
	regular_price_2 = 25
	regular_price_3 = 25
	discount_price_1 = 20
	discount_price_2 = 20
	discount_price_3 = 20
	type_1 = None
	category_1 = None
	category_2 = None
	
	@classmethod
	def setUpTestData(cls):
		cls.user = MyUser.objects.create_user(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
			is_active=True
		)
		
		cls.category_1 = Category.objects.create(name=cls.category_name_1)
		cls.category_2 = Category.objects.create(name=cls.category_name_2, is_active=False)
		cls.type_1 = ProductType.objects.create(name=cls.type_name_1)
		
		cls.product_1 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_1,
			title=cls.title_1,
			description=cls.description_1,
			regular_price=cls.regular_price_1,
			discount_price=cls.discount_price_1
		)
		
		cls.product_2 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_1,
			title=cls.title_2,
			description=cls.description_2,
			regular_price=cls.regular_price_2,
			discount_price=cls.discount_price_2,
			is_active=False
		)
		
		cls.product_3 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_2,
			title=cls.title_3,
			description=cls.description_3,
			regular_price=cls.regular_price_3,
			discount_price=cls.discount_price_3
		)
	
	def setUp(self):
		self.url = reverse('store:category', args=[self.category_1.slug])
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_context(self):
		context = self.response.context
		self.assertIn('category', context)
		self.assertIn('products', context)
		self.assertEqual(len(context['products']), 1)
	
	def test_404(self):
		inactive = reverse('store:category', args=[self.category_2.slug])
		response = self.client.get(inactive)
		self.assertEqual(response.status_code, 404)

		wrong = reverse('store:category', args=['does-not-exist'])
		response = self.client.get(wrong)
		self.assertEqual(response.status_code, 404)
	
	def test_template_register(self):
		self.assertTemplateUsed(self.response, 'store/category.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')
	
	
	
	