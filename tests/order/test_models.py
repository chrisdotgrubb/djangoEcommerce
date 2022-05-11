from django.test import TestCase
from ecommerce.apps.checkout.models import DeliveryOptions
from ecommerce.apps.order.models import Order, OrderItem, OrderItemManager
from ecommerce.apps.store.models import Category, Product, ProductType
from ecommerce.apps.user.models import MyUser


class TestOrder(TestCase):
	name_1 = None
	username_1 = None
	password_1 = None
	email_1 = None
	first_1 = None
	address1_1 = None
	address2_1 = None
	city_1 = None
	state_1 = None
	country_1 = None
	zip_code_1 = None
	delivery_instructions_1 = None
	total_paid_1 = None
	order_key_1 = None
	payment_option_1 = None
	user_1 = None
	delivery_option_1 = None
	is_paid = None
	
	@classmethod
	def setUpTestData(cls):
		cls.email_1 = 'user_1@user.com'
		cls.username_1 = 'user_1'
		cls.password_1 = 'password'
		cls.first_1 = 'first'
		cls.name_1 = 'first last'
		cls.address1_1 = '123 Main Street'
		cls.address2_1 = 'Apt. 1'
		cls.city_1 = 'Bellefonte'
		cls.state_1 = 'PA'
		cls.country_1 = 'US'
		cls.zip_code_1 = '16823'
		cls.delivery_instructions_1 = 'Front Door'
		cls.total_paid_1 = 100
		cls.order_key_1 = 'key_from_PayPal'
		cls.payment_option_1 = 'PayPal'
		cls.is_paid = True
		
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
	name_1 = None
	username_1 = None
	password_1 = None
	email_1 = None
	first_1 = None
	address1_1 = None
	address2_1 = None
	city_1 = None
	state_1 = None
	country_1 = None
	zip_code_1 = None
	delivery_instructions_1 = None
	total_paid_1 = None
	order_key_1 = None
	payment_option_1 = None
	user_1 = None
	delivery_option_1 = None
	is_paid = None
	order_1 = None
	qty_1 = None
	category_name_1 = None
	type_name_1 = None
	title_1 = None
	title_2 = None
	title_3 = None
	description_1 = None
	description_2 = None
	description_3 = None
	regular_price_1 = None
	discount_price_1 = None
	type_1 = None
	category_1 = None
	product_1 = None
	product_2 = None
	product_3 = None
	
	@classmethod
	def setUpTestData(cls):
		cls.email_1 = 'user_1@user.com'
		cls.username_1 = 'user_1'
		cls.password_1 = 'password'
		cls.first_1 = 'first'
		cls.name_1 = 'first last'
		cls.address1_1 = '123 Main Street'
		cls.address2_1 = 'Apt. 1'
		cls.city_1 = 'Bellefonte'
		cls.state_1 = 'PA'
		cls.country_1 = 'US'
		cls.zip_code_1 = '16823'
		cls.delivery_instructions_1 = 'Front Door'
		cls.total_paid_1 = 100
		cls.order_key_1 = 'key_from_PayPal'
		cls.payment_option_1 = 'PayPal'
		cls.is_paid = True
		cls.qty_1 = 1
		cls.category_name_1 = 'category'
		cls.type_name_1 = 'type'
		cls.title_1 = 'product 1'
		cls.title_2 = 'product 2'
		cls.title_3 = 'product 3'
		cls.description_1 = 'description 1'
		cls.description_2 = 'description 2'
		cls.description_3 = 'description 3'
		cls.regular_price_1 = 25
		cls.discount_price_1 = 20
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
