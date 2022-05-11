from django.test import TestCase
from ecommerce.apps.store.models import Category, Product, ProductSpecification, ProductSpecificationValue, ProductType


class TestCategoryModel(TestCase):
	name_1 = None
	name_2 = None
	name_3 = None
	name_4 = None
	
	@classmethod
	def setUpTestData(cls):
		cls.name_1 = 'category'
		cls.name_2 = 'Category'
		cls.name_3 = 'CATEGORY'
		cls.name_4 = 'cat'
		cls.category_1 = Category.objects.create(name=cls.name_1)
		cls.category_2 = Category.objects.create(name=cls.name_2)
		cls.category_3 = Category.objects.create(name=cls.name_3)
		cls.category_4 = Category.objects.create(name=cls.name_4)
	
	def test_slug(self):
		self.assertEqual(self.category_1.slug, 'category')
		self.assertEqual(self.category_2.slug, 'category-1')
		self.assertEqual(self.category_3.slug, 'category-2')
		self.assertEqual(self.category_4.slug, 'cat-3')
	
	def test_str(self):
		self.assertEqual(str(self.category_1), self.name_1)
		self.assertEqual(str(self.category_2), self.name_2)
		self.assertEqual(str(self.category_3), self.name_3)
		self.assertEqual(str(self.category_4), self.name_4)
	
	def test_get_absolute_url(self):
		self.assertEqual(self.category_1.get_absolute_url(), f'/shop/{self.category_1.slug}/')
		self.assertEqual(self.category_2.get_absolute_url(), f'/shop/{self.category_2.slug}/')
		self.assertEqual(self.category_3.get_absolute_url(), f'/shop/{self.category_3.slug}/')
		self.assertEqual(self.category_4.get_absolute_url(), f'/shop/{self.category_4.slug}/')


class TestProductType(TestCase):
	name_1 = None
	name_2 = None
	name_3 = None
	
	@classmethod
	def setUpTestData(cls):
		cls.name_1 = 'type1'
		cls.name_2 = 'type2'
		cls.name_3 = 'type3'
		
		cls.type_1 = ProductType.objects.create(name=cls.name_1)
		cls.type_2 = ProductType.objects.create(name=cls.name_2)
		cls.type_3 = ProductType.objects.create(name=cls.name_3)
	
	def test_str(self):
		self.assertEqual(str(self.type_1), self.name_1)
		self.assertEqual(str(self.type_2), self.name_2)
		self.assertEqual(str(self.type_3), self.name_3)


class TestProductSpecification(TestCase):
	name_1 = None
	name_2 = None
	name_3 = None
	type_1 = None
	
	@classmethod
	def setUpTestData(cls):
		cls.name_1 = 'type1'
		cls.name_2 = 'type2'
		cls.name_3 = 'type3'
		
		cls.type_1 = ProductType.objects.create(name='type_1')
		
		cls.spec_1 = ProductSpecification.objects.create(product_type=cls.type_1, name=cls.name_1)
		cls.spec_2 = ProductSpecification.objects.create(product_type=cls.type_1, name=cls.name_2)
		cls.spec_3 = ProductSpecification.objects.create(product_type=cls.type_1, name=cls.name_3)
	
	def test_str(self):
		self.assertEqual(str(self.spec_1), self.name_1)
		self.assertEqual(str(self.spec_2), self.name_2)
		self.assertEqual(str(self.spec_3), self.name_3)


class TestProduct(TestCase):
	category_name_1 = None
	type_name_1 = None
	title_1 = None
	title_2 = None
	title_3 = None
	title_4 = None
	title_5 = None
	description_1 = None
	description_2 = None
	description_3 = None
	description_4 = None
	description_5 = None
	regular_price_1 = None
	regular_price_2 = None
	regular_price_3 = None
	regular_price_4 = None
	regular_price_5 = None
	discount_price_1 = None
	discount_price_2 = None
	discount_price_3 = None
	discount_price_4 = None
	discount_price_5 = None
	type_1 = None
	category_1 = None
	
	@classmethod
	def setUpTestData(cls):
		cls.category_name_1 = 'category'
		cls.type_name_1 = 'type'
		cls.title_1 = 'product 1'
		cls.title_2 = 'product 1'
		cls.title_3 = 'product-1'
		cls.title_4 = 'product-1'
		cls.title_5 = 'pro'
		cls.description_1 = 'description 1'
		cls.description_2 = 'description 2'
		cls.description_3 = 'description 3'
		cls.description_4 = 'description 4'
		cls.description_5 = 'description 5'
		cls.regular_price_1 = 25
		cls.regular_price_2 = 25
		cls.regular_price_3 = 25
		cls.regular_price_4 = 25
		cls.regular_price_5 = 25
		cls.discount_price_1 = 20
		cls.discount_price_2 = 20
		cls.discount_price_3 = 20
		cls.discount_price_4 = 20
		cls.discount_price_5 = 20
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
			discount_price=cls.discount_price_3
		)
		
		cls.product_4 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_1,
			title=cls.title_4,
			description=cls.description_4,
			regular_price=cls.regular_price_4,
			discount_price=cls.discount_price_4
		)
		
		cls.product_5 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_1,
			title=cls.title_5,
			description=cls.description_5,
			regular_price=cls.regular_price_5,
			discount_price=cls.discount_price_5
		)
	
	def test_slug(self):
		self.assertEqual(self.product_1.slug, f'product-1')
		self.assertEqual(self.product_2.slug, f'product-1-1')
		self.assertEqual(self.product_3.slug, f'product-1-2')
		self.assertEqual(self.product_4.slug, f'product-1-3')
		self.assertEqual(self.product_5.slug, f'pro-4')
	
	def test_str(self):
		self.assertEqual(str(self.product_1), self.title_1)
		self.assertEqual(str(self.product_2), self.title_2)
		self.assertEqual(str(self.product_3), self.title_3)
		self.assertEqual(str(self.product_4), self.title_4)
		self.assertEqual(str(self.product_5), self.title_5)
	
	def test_get_absolute_url(self):
		self.assertEqual(self.product_1.get_absolute_url(), f'/{self.product_1.slug}/')
		self.assertEqual(self.product_2.get_absolute_url(), f'/{self.product_2.slug}/')
		self.assertEqual(self.product_3.get_absolute_url(), f'/{self.product_3.slug}/')
		self.assertEqual(self.product_4.get_absolute_url(), f'/{self.product_4.slug}/')
		self.assertEqual(self.product_5.get_absolute_url(), f'/{self.product_5.slug}/')


class TestProductSpecificationValue(TestCase):
	category_name_1 = None
	type_name_1 = None
	title_1 = None
	description_1 = None
	regular_price_1 = None
	discount_price_1 = None
	type_1 = None
	category_1 = None
	spec_name_1 = None
	spec_value_1 = None
	product_1 = None
	product_spec_val_1 = None
	
	@classmethod
	def setUpTestData(cls):
		cls.category_name_1 = 'category'
		cls.type_name_1 = 'type'
		cls.title_1 = 'product 1'
		cls.description_1 = 'description 1'
		cls.regular_price_1 = 25
		cls.discount_price_1 = 20
		cls.spec_name_1 = 'specification 1'
		cls.spec_value_1 = 'specification 1'
		cls.category_1 = Category.objects.create(name=cls.category_name_1)
		cls.type_1 = ProductType.objects.create(name=cls.type_name_1)
		cls.product_spec_val_1 = ProductSpecification.objects.create(product_type=cls.type_1, name=cls.spec_name_1)

		cls.product_1 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_1,
			title=cls.title_1,
			description=cls.description_1,
			regular_price=cls.regular_price_1,
			discount_price=cls.discount_price_1
		)
	
		cls.spec_value = ProductSpecificationValue.objects.create(
			product=cls.product_1,
			specification=cls.product_spec_val_1,
			value=cls.spec_value_1,
		)

	def test_str(self):
		self.assertEqual(str(self.spec_value), self.spec_value_1)
	