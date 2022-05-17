from django.test import TestCase
from django.urls import reverse

from ecommerce.apps.store.models import Category, Product, ProductType
from ecommerce.apps.user.models import MyUser


class TestCart(TestCase):
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
			discount_price=cls.discount_price_2
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
		self.url = reverse('cart:cart')
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_context(self):
		context = self.response.context
		self.assertIn('cart', context)
		self.assertIn('form', context)
	
	def test_session(self):
		session = self.client.session
		self.assertIn('cart', session)
		self.assertEqual(session['cart'], {})
	
	def test_product_in_products(self):
		session = self.client.session
		session['cart'][1] = {'name': self.product_1.slug, 'qty': 1}
		session['cart'][2] = {'name': self.product_2.slug, 'qty': 1}
		session['cart'][3] = {'name': self.product_3.slug, 'qty': 1}
		session.save()
		response = self.client.get(self.url)
		
		self.assertEqual(len(response.context['cart']), 3)
		product_from_cart = response.context['cart'].cart['1']['product']
		self.assertEqual(self.product_1, product_from_cart)
		
		product_from_cart = response.context['cart'].cart['2']['product']
		self.assertEqual(self.product_2, product_from_cart)
		
		product_from_cart = response.context['cart'].cart['3']['product']
		self.assertEqual(self.product_3, product_from_cart)
	
	def test_template_register(self):
		self.assertTemplateUsed(self.response, 'cart/cart.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')


class TestCartAdd(TestCase):
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
			discount_price=cls.discount_price_2
		)
		
		cls.product_3 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_2,
			title=cls.title_3,
			description=cls.description_3,
			regular_price=cls.regular_price_3,
			discount_price=cls.discount_price_3,
			is_active=False
		)
	
	def setUp(self):
		self.url = reverse('cart:add', args=[self.product_1.pk])
	
	def test_post(self):
		response = self.client.post(self.url)
		self.assertEqual(response.status_code, 200)
	
	def test_qty(self):
		qty_1 = 1
		self.client.post(self.url, {'qty': qty_1})
		self.assertEqual((self.client.session['cart']['1']['qty']), qty_1)
		
		qty_2 = 20
		self.client.post(self.url, {'qty': qty_2})
		self.assertEqual((self.client.session['cart']['1']['qty']), qty_1 + qty_2)
		
		url = reverse('cart:add', args=[2])
		self.client.post(url, {'qty': qty_1})
		self.assertEqual((self.client.session['cart']['1']['qty']), qty_1 + qty_2)
		self.assertEqual((self.client.session['cart']['2']['qty']), qty_1)
		
		self.client.post(url, {'qty': qty_2})
		self.assertEqual((self.client.session['cart']['1']['qty']), qty_1 + qty_2)
		self.assertEqual((self.client.session['cart']['2']['qty']), qty_1 + qty_2)
	
	def test_context(self):
		response = self.client.post(self.url)
		context = response.context
		self.assertIn('product', context)
		self.assertIn('form', context)
	
	def test_404(self):
		inactive = reverse('cart:add', args=[self.product_3.pk])
		response = self.client.post(inactive, {'qty': 1})
		self.assertEqual(response.status_code, 404)
		
		wrong = reverse('cart:add', args=[999])
		response = self.client.post(wrong, {'qty': 1})
		self.assertEqual(response.status_code, 404)
	
	def test_http_methods(self):
		response = self.client.get(self.url, {'qty': 1})
		self.assertEqual(response.status_code, 405)


class TestCartDelete(TestCase):
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
			discount_price=cls.discount_price_2
		)
		
		cls.product_3 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_2,
			title=cls.title_3,
			description=cls.description_3,
			regular_price=cls.regular_price_3,
			discount_price=cls.discount_price_3,
			is_active=False
		)
	
	def setUp(self):
		self.url = reverse('cart:delete', args=[self.product_1.pk])
		self.client.get(reverse('cart:cart'))
	
	def test_post(self):
		response = self.client.delete(self.url)
		self.assertEqual(response.status_code, 200)
	
	def test_qty(self):
		session = self.client.session
		session['cart'][1] = {'name': self.product_1.slug, 'qty': 1}
		session['cart'][2] = {'name': self.product_2.slug, 'qty': 1}
		session['cart'][3] = {'name': self.product_3.slug, 'qty': 2}
		session.save()
		self.assertEqual(len(self.client.session['cart']), 3)
		
		url = reverse('cart:delete', args=[self.product_1.pk])
		self.client.delete(url)
		self.assertEqual(len(self.client.session['cart']), 2)
		
		url = reverse('cart:delete', args=[self.product_2.pk])
		self.client.delete(url)
		self.assertEqual(len(self.client.session['cart']), 1)
		
		url = reverse('cart:delete', args=[self.product_3.pk])
		self.client.delete(url)
		self.assertEqual(len(self.client.session['cart']), 0)
	
	def test_htmx_trigger(self):
		response = self.client.delete(self.url)
		self.assertIn('cartUpdatedEvent', response.headers['hx-trigger'])
	
	def test_http_methods(self):
		response = self.client.get(self.url, {'qty': 1})
		self.assertEqual(response.status_code, 405)
		
		response = self.client.post(self.url, {'qty': 1})
		self.assertEqual(response.status_code, 405)


class TestCartChooseQuantity(TestCase):
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
			discount_price=cls.discount_price_2
		)
		
		cls.product_3 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_2,
			title=cls.title_3,
			description=cls.description_3,
			regular_price=cls.regular_price_3,
			discount_price=cls.discount_price_3,
			is_active=False
		)
	
	def setUp(self):
		self.url = reverse('cart:choose_qty', args=[self.product_1.pk])
		self.client.get(reverse('cart:cart'))
	
	def test_post(self):
		response = self.client.post(self.url)
		self.assertEqual(response.status_code, 200)
	
	def test_qty(self):
		session = self.client.session
		session['cart'][1] = {'name': self.product_1.slug, 'qty': 1}
		session['cart'][2] = {'name': self.product_2.slug, 'qty': 1}
		session['cart'][3] = {'name': self.product_3.slug, 'qty': 2}
		session.save()
		self.assertEqual((self.client.session['cart']['1']['qty']), 1)
		
		qty_1 = 5
		url = reverse('cart:choose_qty', args=[self.product_1.pk])
		self.client.post(url, {'qty': qty_1})
		self.assertEqual(self.client.session['cart']['1']['qty'], qty_1)
		self.assertEqual(self.client.session['cart']['2']['qty'], 1)
		self.assertEqual(self.client.session['cart']['3']['qty'], 2)
	
	def test_context(self):
		response = self.client.post(self.url)
		context = response.context
		self.assertIn('product', context)
		self.assertIn('form', context)
	
	def test_404(self):
		inactive = reverse('cart:choose_qty', args=[self.product_3.pk])
		response = self.client.post(inactive, {'qty': 1})
		self.assertEqual(response.status_code, 404)
		
		wrong = reverse('cart:choose_qty', args=[999])
		response = self.client.post(wrong, {'qty': 1})
		self.assertEqual(response.status_code, 404)
	
	def test_htmx_trigger(self):
		response = self.client.post(self.url)
		self.assertIn('cartUpdatedEvent', response.headers['hx-trigger'])
		
	def test_htmx_trigger_0(self):
		response = self.client.post(self.url, {'qty': 0})
		self.assertIn('cartUpdatedEvent', response.headers['hx-trigger'])
		self.assertIn(f'deletedEvent-{self.product_1.pk}', response.headers['hx-trigger'])
		
	def test_http_methods(self):
		response = self.client.get(self.url, {'qty': 1})
		self.assertEqual(response.status_code, 405)
		
	def test_template_quantity(self):
		response = self.client.post(self.url)
		self.assertTemplateUsed(response, 'cart/_quantity.html')


class TestCartUpdateNumber(TestCase):
	def setUp(self):
		self.url = reverse('cart:update_total')
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
		
	def test_template_total(self):
		self.assertTemplateUsed(self.response, 'cart/_total.html')


class TestCartUpdateDetails(TestCase):
	def setUp(self):
		self.url = reverse('cart:update_details')
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_template_details(self):
		self.assertTemplateUsed(self.response, 'cart/_details.html')


class TestCartUpdateFooter(TestCase):
	def setUp(self):
		self.url = reverse('cart:update_footer')
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'cart/_footer.html')


class TestCartUpdateItemTotal(TestCase):
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
			discount_price=cls.discount_price_2
		)
		
		cls.product_3 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_2,
			title=cls.title_3,
			description=cls.description_3,
			regular_price=cls.regular_price_3,
			discount_price=cls.discount_price_3,
			is_active=False
		)
	
	def setUp(self):
		self.client.get(reverse('cart:cart'))
		session = self.client.session
		session['cart'][1] = {'name': self.product_1.slug, 'qty': 1}
		session['cart'][2] = {'name': self.product_2.slug, 'qty': 1}
		session['cart'][3] = {'name': self.product_3.slug, 'qty': 2}
		session.save()
		self.url = reverse('cart:update_item_total', args=[self.product_1.pk])
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_pid_not_in_cart(self):
		self.assertEqual(len(self.response.context['cart']), 3)
		url = reverse('cart:update_item_total', args=[999])
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(response.context['cart']), 3)

		
	def test_template_register(self):
		self.assertTemplateUsed(self.response, 'cart/_item_total.html')

		