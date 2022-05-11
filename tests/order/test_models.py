from django.test import TestCase
from ecommerce.apps.checkout.models import DeliveryOptions
from ecommerce.apps.order.models import Order, OrderItem, OrderItemManager
from ecommerce.apps.store.models import Category, Product, ProductType
from ecommerce.apps.user.models import MyUser


class TestOrder(TestCase):
	email_1 = 'user_1@user.com'
	username_1 = 'user_1'
	password_1 = 'password'
	first_1 = 'first'
	name_1 = 'first last'
	address1_1 = '123 Main Street'
	address2_1 = 'Apt. 1'
	city_1 = 'Bellefonte'
	state_1 = 'PA'
	country_1 = 'US'
	zip_code_1 = '16823'
	delivery_instructions_1 = 'Front Door'
	total_paid_1 = 100
	order_key_1 = 'key_from_PayPal'
	payment_option_1 = 'PayPal'
	is_paid = True
	user_1 = None
	delivery_option_1 = None
	
	@classmethod
	def setUpTestData(cls):
		cls.user_1 = MyUser.objects.create_user(cls.email_1, cls.username_1, cls.password_1)
		cls.delivery_option_1 = DeliveryOptions.objects.create(
			delivery_method='PA',
			delivery_name='Ground Shipping',
			delivery_price=9.99,
			delivery_timeframe='3-5 Business Days',
			delivery_window='8-5',
			order=1
		)
		
		cls.order_1 = Order.objects.create(
			user=cls.user_1,
			name=cls.name_1,
			email=cls.email_1,
			address1=cls.address1_1,
			address2=cls.address2_1,
			city=cls.city_1,
			state=cls.state_1,
			country=cls.country_1,
			zip_code=cls.zip_code_1,
			delivery_instructions=cls.delivery_instructions_1,
			total_paid=cls.total_paid_1,
			order_key=cls.order_key_1,
			payment_option=cls.payment_option_1,
			delivery_option=cls.delivery_option_1,
			is_paid=cls.is_paid
		)
	
	def test_str(self):
		self.assertEqual(str(self.order_1), f'{self.name_1} {self.order_1.created:%Y %b %d %H:%M}')


class TestOrderItem(TestCase):
	email_1 = 'user_1@user.com'
	username_1 = 'user_1'
	password_1 = 'password'
	first_1 = 'first'
	name_1 = 'first last'
	address1_1 = '123 Main Street'
	address2_1 = 'Apt. 1'
	city_1 = 'Bellefonte'
	state_1 = 'PA'
	country_1 = 'US'
	zip_code_1 = '16823'
	delivery_instructions_1 = 'Front Door'
	total_paid_1 = 100
	order_key_1 = 'key_from_PayPal'
	payment_option_1 = 'PayPal'
	is_paid = True
	qty_1 = 1
	category_name_1 = 'category'
	type_name_1 = 'type'
	title_1 = 'product 1'
	title_2 = 'product 2'
	title_3 = 'product 3'
	description_1 = 'description 1'
	description_2 = 'description 2'
	description_3 = 'description 3'
	regular_price_1 = 25
	discount_price_1 = 20
	type_1 = None
	category_1 = None
	user_1 = None
	delivery_option_1 = None
	order_1 = None
	product_1 = None
	product_2 = None
	product_3 = None

	@classmethod
	def setUpTestData(cls):
		cls.category_1 = Category.objects.create(name=cls.category_name_1)
		cls.type_1 = ProductType.objects.create(name=cls.type_name_1)
		
		cls.user_1 = MyUser.objects.create_user(cls.email_1, cls.username_1, cls.password_1)
		cls.delivery_option_1 = DeliveryOptions.objects.create(
			delivery_method='PA',
			delivery_name='Ground Shipping',
			delivery_price=9.99,
			delivery_timeframe='3-5 Business Days',
			delivery_window='8-5',
			order=1
		)
		
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
			regular_price=cls.regular_price_1,
			discount_price=cls.discount_price_1
		)
		
		cls.product_3 = Product.objects.create(
			product_type=cls.type_1,
			category=cls.category_1,
			title=cls.title_3,
			description=cls.description_3,
			regular_price=cls.regular_price_1,
			discount_price=cls.discount_price_1
		)
		
		cls.order_1 = Order.objects.create(
			user=cls.user_1,
			name=cls.name_1,
			email=cls.email_1,
			address1=cls.address1_1,
			address2=cls.address2_1,
			city=cls.city_1,
			state=cls.state_1,
			country=cls.country_1,
			zip_code=cls.zip_code_1,
			delivery_instructions=cls.delivery_instructions_1,
			total_paid=cls.total_paid_1,
			order_key=cls.order_key_1,
			payment_option=cls.payment_option_1,
			delivery_option=cls.delivery_option_1,
			is_paid=cls.is_paid
		)
		
		cls.order_item_1 = OrderItem.objects.create(
			order=cls.order_1,
			product=cls.product_1,
			price=cls.product_1.regular_price,
			quantity=cls.qty_1
		)
		
		cls.order_item_2 = OrderItem.objects.create(
			order=cls.order_1,
			product=cls.product_2,
			price=cls.product_2.regular_price,
			quantity=cls.qty_1
		)
		
		cls.order_item_3 = OrderItem.objects.create(
			order=cls.order_1,
			product=cls.product_3,
			price=cls.product_3.regular_price,
			quantity=cls.qty_1
		)
	
	def test_str(self):
		self.assertEqual(str(self.order_item_1), f'{self.product_1.title} - {self.order_1}')
		self.assertEqual(str(self.order_item_2), f'{self.product_2.title} - {self.order_1}')
		self.assertEqual(str(self.order_item_3), f'{self.product_3.title} - {self.order_1}')
	
	def test_order_item_manager_get_queryset(self):
		objects_qs = OrderItem.objects.filter(order=self.order_1, product__is_active=True)
		products_qs = OrderItem.products.filter(order=self.order_1)
		self.assertEqual(len(products_qs), len(objects_qs))
		self.assertEqual(len(products_qs), 3)
