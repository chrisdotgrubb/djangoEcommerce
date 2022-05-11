from django.core import mail

from ecommerce.apps.user.models import Address, MyUser
from django.test import TestCase
from django.utils.translation import gettext_lazy as _

class TestMyUser(TestCase):
	email = 'test@test.com'
	username = 'test'
	password = 'password'
	phone = '814-574-0000'
	first = 'first'
	
	@classmethod
	def setUpTestData(cls):
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
		
	def test_create_user_value_errors(self):
		blank = ''
		email = 'email@email.com'
		username = 'username'
		password = 'password'
		
		self.assertRaises(ValueError, MyUser.objects.create_user, blank, username, password)
		self.assertRaises(ValueError, MyUser.objects.create_user, email=email, username=blank, password=password)
		with self.assertRaises(ValueError):
			MyUser.objects.create_user(email=email, username=username, password=blank)
	
	def test_normalize_email(self):
		expected = 'normal@gmail.com'
		bad_1 = '     normal@gmail.com'
		bad_2 = 'normal@gmail.com    '
		bad_3 = '     normal@gmail.com      '
		bad_4 = 'normal@GMAIL.COM'
		bad_5 = '     normal@GMAIL.COM      '
		
		user_1 = MyUser.objects.create_user(bad_1, 'bad_1', 'password')
		self.assertEqual(user_1.email, expected)
		user_1.delete()
		user_2 = MyUser.objects.create_user(bad_2, 'bad_2', 'password')
		self.assertEqual(user_2.email, expected)
		user_2.delete()
		user_3 = MyUser.objects.create_user(bad_3, 'bad_3', 'password')
		self.assertEqual(user_3.email, expected)
		user_3.delete()
		user_4 = MyUser.objects.create_user(bad_4, 'bad_4', 'password')
		self.assertEqual(user_4.email, expected)
		user_4.delete()
		user_5 = MyUser.objects.create_user(bad_5, 'bad_5', 'password')
		self.assertEqual(user_5.email, expected)
		user_5.delete()
	
	def test_set_password(self):
		self.assertTrue(self.user.check_password('password'))
		self.user.set_password('different')
		self.assertTrue(self.user.check_password('different'))
		self.user.set_password(self.password)
		
	def test_create_superuser(self):
		email = 'super@super.com'
		username = 'super'
		password = 'password'
		self.assertFalse(self.user.is_staff)
		self.assertFalse(self.user.is_superuser)
		superuser = MyUser.objects.create_superuser(email, username, password)
		self.assertTrue(superuser.is_staff)
		self.assertTrue(superuser.is_superuser)
	
	def test_email_user(self):
		self.user.email_user('subject', 'message')
		self.assertEqual(len(mail.outbox), 1)
		self.assertEqual(mail.outbox[0].subject, 'subject')
		self.assertEqual(mail.outbox[0].body, 'message')
	

class TestAddress(TestCase):
	email = 'test@test.com'
	username = 'test'
	password = 'password'
	name = 'name'
	phone = '814-574-0000'
	country = 'US'
	address_line_1 = '123 Main Street.'
	address_line_2 = 'Apartment 3'
	town_city = 'Bellefonte'
	state = 'PA'
	zip = '16823'
	delivery_instructions = 'Leave on porch'
	user_1 = None
	
	@classmethod
	def setUpTestData(cls):
		cls.user_1 = MyUser.objects.create_user(cls.email, cls.username, cls.password)
		cls.address = Address.objects.create(
			customer=cls.user_1,
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
		self.assertEqual(self.address.customer, self.user_1)
		
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
	
	def test_formatted_phone(self):
		expected = '(555) 555-5555'
		format_1 = '5555555555'
		format_2 = '555-555-5555'
		format_3 = '(555)555-5555'
		format_4 = '(555)-555-5555'
		format_5 = '555 555 5555'
		format_6 = '555.555.5555'
		format_7 = '1.555.555.5555'
		format_8 = '1-555-5555-555'
		format_9 = '+1-555-5555-555'
		format_10 = '+1555.555.5555'
		format_11 = '+1.555.555.5555'
		format_12 = '+15555555555'

		address_1 = Address.objects.create(
			customer=self.user_1,
			name=self.name,
			phone=format_1,
			country=self.country,
			address_line_1=self.address_line_1,
			address_line_2=self.address_line_2,
			town_city=self.town_city,
			state=self.state,
			zip=self.zip,
			delivery_instructions=self.delivery_instructions,
		)
		
		address_2 = Address.objects.create(
			customer=self.user_1,
			name=self.name,
			phone=format_2,
			country=self.country,
			address_line_1=self.address_line_1,
			address_line_2=self.address_line_2,
			town_city=self.town_city,
			state=self.state,
			zip=self.zip,
			delivery_instructions=self.delivery_instructions,
		)
		
		address_3 = Address.objects.create(
			customer=self.user_1,
			name=self.name,
			phone=format_3,
			country=self.country,
			address_line_1=self.address_line_1,
			address_line_2=self.address_line_2,
			town_city=self.town_city,
			state=self.state,
			zip=self.zip,
			delivery_instructions=self.delivery_instructions,
		)
		
		address_4 = Address.objects.create(
			customer=self.user_1,
			name=self.name,
			phone=format_4,
			country=self.country,
			address_line_1=self.address_line_1,
			address_line_2=self.address_line_2,
			town_city=self.town_city,
			state=self.state,
			zip=self.zip,
			delivery_instructions=self.delivery_instructions,
		)
		
		address_5 = Address.objects.create(
			customer=self.user_1,
			name=self.name,
			phone=format_5,
			country=self.country,
			address_line_1=self.address_line_1,
			address_line_2=self.address_line_2,
			town_city=self.town_city,
			state=self.state,
			zip=self.zip,
			delivery_instructions=self.delivery_instructions,
		)
		
		address_6 = Address.objects.create(
			customer=self.user_1,
			name=self.name,
			phone=format_6,
			country=self.country,
			address_line_1=self.address_line_1,
			address_line_2=self.address_line_2,
			town_city=self.town_city,
			state=self.state,
			zip=self.zip,
			delivery_instructions=self.delivery_instructions,
		)
		
		address_7 = Address.objects.create(
			customer=self.user_1,
			name=self.name,
			phone=format_7,
			country=self.country,
			address_line_1=self.address_line_1,
			address_line_2=self.address_line_2,
			town_city=self.town_city,
			state=self.state,
			zip=self.zip,
			delivery_instructions=self.delivery_instructions,
		)
		
		address_8 = Address.objects.create(
			customer=self.user_1,
			name=self.name,
			phone=format_8,
			country=self.country,
			address_line_1=self.address_line_1,
			address_line_2=self.address_line_2,
			town_city=self.town_city,
			state=self.state,
			zip=self.zip,
			delivery_instructions=self.delivery_instructions,
		)
		
		address_9 = Address.objects.create(
			customer=self.user_1,
			name=self.name,
			phone=format_9,
			country=self.country,
			address_line_1=self.address_line_1,
			address_line_2=self.address_line_2,
			town_city=self.town_city,
			state=self.state,
			zip=self.zip,
			delivery_instructions=self.delivery_instructions,
		)
		
		address_10 = Address.objects.create(
			customer=self.user_1,
			name=self.name,
			phone=format_10,
			country=self.country,
			address_line_1=self.address_line_1,
			address_line_2=self.address_line_2,
			town_city=self.town_city,
			state=self.state,
			zip=self.zip,
			delivery_instructions=self.delivery_instructions,
		)
		
		address_11 = Address.objects.create(
			customer=self.user_1,
			name=self.name,
			phone=format_11,
			country=self.country,
			address_line_1=self.address_line_1,
			address_line_2=self.address_line_2,
			town_city=self.town_city,
			state=self.state,
			zip=self.zip,
			delivery_instructions=self.delivery_instructions,
		)
		
		address_12 = Address.objects.create(
			customer=self.user_1,
			name=self.name,
			phone=format_12,
			country=self.country,
			address_line_1=self.address_line_1,
			address_line_2=self.address_line_2,
			town_city=self.town_city,
			state=self.state,
			zip=self.zip,
			delivery_instructions=self.delivery_instructions,
		)
		
		self.assertEqual(address_1.formatted_phone(), expected)
		self.assertEqual(address_2.formatted_phone(), expected)
		self.assertEqual(address_3.formatted_phone(), expected)
		self.assertEqual(address_4.formatted_phone(), expected)
		self.assertEqual(address_5.formatted_phone(), expected)
		self.assertEqual(address_6.formatted_phone(), expected)
		self.assertEqual(address_7.formatted_phone(), expected)
		self.assertEqual(address_8.formatted_phone(), expected)
		self.assertEqual(address_9.formatted_phone(), expected)
		self.assertEqual(address_10.formatted_phone(), expected)
		self.assertEqual(address_11.formatted_phone(), expected)
		self.assertEqual(address_12.formatted_phone(), expected)
		
		
class TestUserManagers(TestCase):
	
	@classmethod
	def setUpTestData(cls):
		MyUser.objects.create_user('user_1@user.com', 'user_1', 'password', is_active=True)
		MyUser.objects.create_user('user_2@user.com', 'user_2', 'password', is_active=True)
		MyUser.objects.create_user('user_3@user.com', 'user_3', 'password', is_active=True)
		MyUser.objects.create_user('user_4@user.com', 'user_4', 'password', is_active=False)
		MyUser.objects.create_user('user_5@user.com', 'user_5', 'password', is_active=False)
		
	def test_active_manager_qs(self):
		qs = MyUser.active.all()
		self.assertEqual(len(qs), 3)
		
	def test_inactive_manager_qs(self):
		qs = MyUser.inactive.all()
		self.assertEqual(len(qs), 2)
		
		
		