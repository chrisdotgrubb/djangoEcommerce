import os

from django.conf import settings
from django.test import TestCase
from django.urls import resolve, reverse


class TestUrls(TestCase):
	
	def setUp(self):
		pass
		
	def test_admin(self):
		url = '/admin/'
		rev_url = reverse('admin:index')
		self.assertEqual(url, rev_url)
		self.assertRegex(str(resolve(url).func), r'^<function AdminSite\.index at 0x')
		
	def test_media(self):
		self.assertEqual(settings.MEDIA_URL, '/media/')
		self.assertEqual(settings.MEDIA_ROOT, f'{os.getcwd()}\media/')
		