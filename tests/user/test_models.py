from ecommerce.apps.user.models import Address, MyUser
from django.test import TestCase

class TestMyUser(TestCase):
	
	email = None
	username = None
	password = None
	phone = None
	first = None
	
	@classmethod
	def setUpTestData(cls):
		cls.email = 'test@test.com'
		cls.username = 'test'
		cls.password = 'password'
		cls.phone = '814-574-0000'
		cls.first = 'first'
		
		cls.user = MyUser.objects.create_user(
			cls.email,
			cls.username,
			cls.password,
			phone=cls.phone,
			first=cls.first
		)
	
	def test_email(self):
		self.assertEqual(self.user.email, self.email)
		
	def test_username(self):
		self.assertEqual(self.user.username, self.username)
		
	def test_password(self):
		self.assertTrue(self.user.check_password(self.password))
		
	def test_phone(self):
		self.assertEqual(self.user.phone, self.phone)
		
	def test_first(self):
		self.assertEqual(self.user.first, self.first)
		
	def test_str(self):
		self.assertEqual(str(self.user), self.username)
		

class TestAddress(TestCase):
	
	email = None
	username = None
	password = None
	user = None
	name = None
	phone = None
	country = None
	address_line_1 = None
	address_line_2 = None
	town_city = None
	state = None
	zip = None
	delivery_instructions = None
	
	@classmethod
	def setUpTestData(cls):
		cls.email = 'test@test.com'
		cls.username = 'test'
		cls.password = 'password'
		cls.user = MyUser.objects.create_user(cls.email,cls.username,cls.password)
		cls.name = 'name'
		cls.phone = '814-574-0000'
		cls.country = 'US'
		cls.address_line_1 = '123 Main Street.'
		cls.address_line_2 = 'Apartment 3'
		cls.town_city = 'Bellefonte'
		cls.state = 'PA'
		cls.zip = '16823'
		cls.delivery_instructions = 'Leave on porch'
		
		cls.address = Address.objects.create(
			customer=cls.user,
			name=cls.name,
			phone=cls.phone,
			country=cls.country,
			address_line_1=cls.address_line_1,
			address_line_2=cls.address_line_2,
			town_city=cls.town_city,
			state=cls.state,
			zip=cls.zip,
			delivery_instructions=cls.delivery_instructions,
		)
	
	def test_customer(self):
		self.assertEqual(self.address.customer, self.user)
		
	def test_name(self):
		self.assertEqual(self.address.name, self.name)
	
	def test_phone(self):
		self.assertEqual(self.address.phone, self.phone)
		
	def test_country(self):
		self.assertEqual(self.address.country, self.country)
		
	def test_address_line_1(self):
		self.assertEqual(self.address.address_line_1, self.address_line_1)
		
	def test_address_line_2(self):
		self.assertEqual(self.address.address_line_2, self.address_line_2)
	
	def test_town_city(self):
		self.assertEqual(self.address.town_city, self.town_city)
		
	def test_state(self):
		self.assertEqual(self.address.state, self.state)
		
	def test_zip(self):
		self.assertEqual(self.address.zip, self.zip)
		
	def test_delivery_instructions(self):
		self.assertEqual(self.address.delivery_instructions, self.delivery_instructions)
		
	def test_str(self):
		self.assertEqual(str(self.address), f'{self.name} address')
	