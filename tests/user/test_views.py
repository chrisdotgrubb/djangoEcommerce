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
		self.uidb64 = 'MzI4'
		self.url = reverse('user:activate', args=[self.uidb64, self.token])
		self.response = self.client.get(self.url)
		self.assertTemplateUsed('registration/activation_invalid.html')
	
	def test_invalid_uidb64(self):
		self.uidb64 = 'MzI4abc'
		self.url = reverse('user:activate', args=[self.uidb64, self.token])
		self.response = self.client.get(self.url)
		messages = list(self.response.context['messages'])
		self.assertEqual(str(messages[0]), 'Account created, check your email to confirm activation.')
		self.assertEqual(str(messages[1]), 'Account error, may have already been activated.')
		self.assertTemplateUsed('registration/activation_invalid.html')
	
	def test_bad_token(self):
		self.token = 'good_user_but_bad_token'
		self.url = reverse('user:activate', args=[self.uidb64, self.token])
		self.response = self.client.get(self.url)
		messages = list(self.response.context['messages'])
		self.assertEqual(str(messages[0]), 'Account created, check your email to confirm activation.')
		self.assertEqual(str(messages[1]), 'Account error, may have already been activated.')
		self.assertTemplateUsed('registration/activation_invalid.html')


class TestDashboard(TestCase):
	
	def setUp(self):
		user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			password='GoodPassword000',
		)
		self.client.force_login(user)
		self.url = reverse('user:dashboard')
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.status_code, 200)
	
	def test_redirect(self):
		self.client.logout()
		response = self.client.get(self.url)
		self.assertEqual(response.status_code, 302)
	
	def test_template_dashboard(self):
		self.assertTemplateUsed(self.response, 'user/dashboard.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')
	
	
class TestEditProfile(TestCase):
	def setUp(self):
		self.user = MyUser.objects.create_superuser(
			email='email@email.com',
			username='username',
			first='first name',
			password='GoodPassword000',
		)
		self.client.force_login(self.user)
		self.url = reverse('user:edit_profile')
		self.response = self.client.get(self.url)
	
	def test_get(self):
		self.assertEqual(self.response.context['form'].instance, self.user)
		self.assertEqual(self.response.status_code, 200)
	
	def test_post(self):
		data = {
			'username': self.user.username,
			'email': self.user.email,
			'first': 'changed',
			'phone': '(814)574-0000'
			
		}
		response = self.client.post(self.url, data=data)
		user = MyUser.objects.all()[0]
		self.assertEqual(user.username, 'username')
		self.assertEqual(user.email, 'email@email.com')
		self.assertEqual(user.first, 'changed')
		self.assertEqual(user.phone, '(814)574-0000')
		
		self.assertEqual(response.status_code, 200)
		messages = list(response.context['messages'])
		self.assertEqual(str(messages[0]), 'Profile updated.')
	
	def test_form_invalid(self):
		data = {
			'username': self.user.username,
			'email': self.user.email,
			'first': 'changed',
			'phone': '123'
			
		}
		response = self.client.post(self.url, data=data, follow=True)
		user = MyUser.objects.all()[0]
		self.assertEqual(user.username, 'username')
		self.assertEqual(user.email, 'email@email.com')
		self.assertEqual(user.first, 'first name')
		
		self.assertEqual(response.status_code, 200)
		messages = list(response.context['messages'])
		self.assertEqual(str(messages[0]), 'Profile update failed.')

		
	def test_template_edit_profile(self):
		self.assertTemplateUsed(self.response, 'user/edit_profile.html')
	
	def test_template_base(self):
		self.assertTemplateUsed(self.response, 'base.html')
	
	def test_template_footer(self):
		self.assertTemplateUsed(self.response, 'footer.html')
	
	def test_template_navbar(self):
		self.assertTemplateUsed(self.response, 'navbar.html')