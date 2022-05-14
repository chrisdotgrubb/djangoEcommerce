import re

from django.core import mail
from django.test import TestCase
from django.urls import reverse

from ecommerce.apps.user.models import MyUser


class TestUserRegistration(TestCase):
	
	def setUp(self):
		self.url = reverse('user:register')
		self.response = self.client.get(self.url)
		
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
		
	def test_post(self):
		data = {
			'email': 'email@email.com',
			'username': 'username',
			'password1': 'GoodPassword000',
			'password2': 'GoodPassword000'
		}
		users_before = len(MyUser.objects.all())
		response = self.client.post(self.url, data=data)
		self.assertEqual(response.status_code, 302)
		self.assertRedirects(response, reverse('store:products_all'))
		users_after = len(MyUser.objects.all())
		self.assertEqual(users_after, users_before + 1)
		
	def test_is_logged_in(self):
		user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			password='GoodPassword000',
		)
		self.client.force_login(user)
		response = self.client.get(self.url)
		self.assertRedirects(response, reverse('store:products_all'))

	def test_template_register(self):
		self.assertTemplateUsed(self.response, 'registration/register.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')
	
	
class TestAccountActivate(TestCase):
	
	def setUp(self):
		url = reverse('user:register')
		data = {
			'email': 'email@email.com',
			'username': 'username',
			'password1': 'GoodPassword000',
			'password2': 'GoodPassword000'
		}
		self.client.post(url, data=data)
		
		regex = 'http://testserver/user/activate/(.*)/(.*)/'
		results = re.search(regex, mail.outbox[0].body)
		self.uidb64 = results.group(1)
		self.token = results.group(2)
		
	def test_activate_success(self):
		self.url = reverse('user:activate', args=[self.uidb64, self.token])
		self.response = self.client.get(self.url)
		self.assertRedirects(self.response, reverse('user:dashboard'))
		print(self.uidb64)
	
	def test_valid_but_wrong_uidb64(self):
		# also need def test_invalid_uidb64(self):
		self.uidb64 = 'MzI4'
		self.url = reverse('user:activate', args=[self.uidb64, self.token])
		self.response = self.client.get(self.url)
		self.assertTemplateUsed('registration/activation_invalid.html')
		print(self.response)
		print(dir(self.response))
		# should change exception to ValueError, since get_object_or_404 will return 404 before the exception, and change message and possibly template.
		
	def test_invalid_uidb64(self):
		self.uidb64 = 'MzI4'
		# not needed, gets a 404 before adding message. use to check messages later.
		
		# messages = list(self.response.context['messages'])
		# self.assertEqual(str(messages)[0], 'Account error, may have already been activated.')
	
	def test_bad_token(self):
		pass
	
	