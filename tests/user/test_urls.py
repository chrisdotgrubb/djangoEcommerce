from django.test import TestCase
from django.contrib.auth import views as auth_views
from django.urls import resolve, reverse
from ecommerce.apps.user import views


class TestUrls(TestCase):
	
	def setUp(self):
		pass
	
	def test_login_url(self):
		url = '/user/login/'
		rev_url = reverse('user:login')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func.view_class, auth_views.LoginView)
	
	def test_logout_url(self):
		url = '/user/logout/'
		rev_url = reverse('user:logout')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func.view_class, auth_views.LogoutView)
	
	def test_register_url(self):
		url = '/user/register/'
		rev_url = reverse('user:register')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.user_registration_view)
	
	def test_activate_url(self):
		slug = 'slug'
		token = 'token'
		url = f'/user/activate/{slug}/{token}/'
		rev_url = reverse('user:activate', args=[slug, token])
		self.assertEqual(url, rev_url)
	
	def test_password_reset_url(self):
		url = '/user/password_reset/'
		rev_url = reverse('user:password_reset')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetView)
	
	def test_user_password_reset_confirm_url(self):
		slug = 'slug'
		token = 'token'
		url = f'/user/password_reset_confirm/{slug}/{token}/'
		rev_url = reverse('user:password_reset_confirm', args=[slug, token])
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetConfirmView)
	
	def test_password_reset_done_url(self):
		url = '/user/password_reset_done/'
		rev_url = reverse('user:password_reset_done')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetDoneView)
	
	def test_password_reset_complete_url(self):
		url = '/user/password_reset_complete/'
		rev_url = reverse('user:password_reset_complete')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetCompleteView)
	
	def test_password_change_url(self):
		url = '/user/password_change/'
		rev_url = reverse('user:password_change')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func.view_class, auth_views.PasswordChangeView)
	
	def test_password_change_done_url(self):
		url = '/user/password_change_done/'
		rev_url = reverse('user:password_change_done')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func.view_class, auth_views.PasswordChangeDoneView)
	
	def test_dashboard_url(self):
		url = '/user/dashboard/'
		rev_url = reverse('user:dashboard')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.dashboard_view)
	
	def test_profile_edit_url(self):
		url = '/user/profile/edit/'
		rev_url = reverse('user:edit_profile')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.edit_profile_view)
	
	def test_profile_delete_confirm_url(self):
		url = '/user/profile/delete/'
		rev_url = reverse('user:delete_confirm')
		self.assertEqual(url, rev_url)
		response = self.client.get(url)
		self.assertTemplateUsed(response, 'user/delete_confirm.html')
	
	def test_profile_delete_url(self):
		url = '/user/profile/delete/delete/'
		rev_url = reverse('user:delete_profile')
		self.assertEqual(url, rev_url)
	
	def test_profile_delete_finished_url(self):
		url = '/user/profile/delete_finished/'
		rev_url = reverse('user:delete_finished')
		self.assertEqual(url, rev_url)
		response = self.client.get(url)
		self.assertTemplateUsed(response, 'user/delete_finished.html')
	
	def test_addresses_url(self):
		url = '/user/addresses/'
		rev_url = reverse('user:addresses')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.address_list_view)
	
	def test_address_form_url(self):
		url = '/user/address_form/'
		rev_url = reverse('user:address_form')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.address_form)
	
	def test_add_address_url(self):
		url = '/user/add_address/'
		rev_url = reverse('user:add_address')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.add_address)
	
	def test_new_address_url(self):
		url = '/user/new_address_btn/'
		rev_url = reverse('user:new_address_btn')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.new_address_btn)
	
	def test_get_address_url(self):
		uuid = '12345678-1234-1234-1234-123456789012'
		url = f'/user/get_address/{uuid}/'
		rev_url = reverse('user:get_address', args=[uuid])
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.get_address)
	
	def test_edit_address_url(self):
		uuid = '12345678-1234-1234-1234-123456789012'
		url = f'/user/addresses/edit/{uuid}/'
		rev_url = reverse('user:edit_address', args=[uuid])
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.edit_address_view)
	
	def test_delete_address_url(self):
		uuid = '12345678-1234-1234-1234-123456789012'
		url = f'/user/addresses/delete/{uuid}/'
		rev_url = reverse('user:delete_address', args=[uuid])
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.delete_address)
	
	def test_set_default_address_url(self):
		uuid = '12345678-1234-1234-1234-123456789012'
		url = f'/user/addresses/set_default/{uuid}/'
		rev_url = reverse('user:set_default_address', args=[uuid])
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.set_default_address_view)
	
	def test_add_to_wishlist_url(self):
		pk = 0
		url = f'/user/wishlist/add_to_wishlist/{pk}/'
		rev_url = reverse('user:add_to_wishlist', args=[pk])
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.add_to_wishlist_view)
	
	def test_wishlist_url(self):
		url = f'/user/wishlist/'
		rev_url = reverse('user:wishlist')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.wishlist_view)
	
	def test_orders_url(self):
		url = f'/user/orders/'
		rev_url = reverse('user:orders')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.orders_view)
	
	def test_check_username_url(self):
		url = f'/user/check_username/'
		rev_url = reverse('user:check_username')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.check_username)
	
	def test_check_email_url(self):
		url = f'/user/check_email/'
		rev_url = reverse('user:check_email')
		self.assertEqual(url, rev_url)
		self.assertEqual(resolve(url).func, views.check_email)
