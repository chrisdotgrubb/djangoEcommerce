from decimal import Decimal
from django.conf import settings
from django.db import models

from store.models import Product


class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
	name = models.CharField(max_length=150)
	address1 = models.CharField(max_length=250)
	address2 = models.CharField(max_length=250)
	city = models.CharField(max_length=100)
	phone = models.CharField(max_length=100)
	zip_code = models.CharField(max_length=20)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	total_paid = models.DecimalField(max_digits=8, decimal_places=2)
	order_key = models.CharField(max_length=200)
	is_paid = models.BooleanField(default=False)
	
	class Meta:
		ordering = ('-created',)
	
	def __str__(self):
		return f'{self.name}/{self.created}'


class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)
	
	def __str__(self):
		return f'{self.product.title}'