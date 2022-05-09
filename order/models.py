from django.conf import settings
from django.db import models
from django_countries.fields import CountryField
from localflavor.us.models import USStateField

from checkout.models import DeliveryOptions
from store.models import Product


class Order(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='order_user')
	
	name = models.CharField(max_length=150)
	email = models.EmailField(max_length=254, blank=True)
	address1 = models.CharField(max_length=250, blank=True)
	address2 = models.CharField(max_length=250, blank=True)
	city = models.CharField(max_length=100)
	state = USStateField()
	country = CountryField()
	zip_code = models.CharField(max_length=20)
	delivery_instructions = models.CharField(max_length=255, blank=True)
	total_paid = models.DecimalField(max_digits=8, decimal_places=2)
	order_key = models.CharField(max_length=200)
	payment_option = models.CharField(max_length=200, blank=True)
	delivery_option = models.ForeignKey(DeliveryOptions, on_delete=models.CASCADE, related_name='delivery_option')
	is_paid = models.BooleanField(default=False)
	
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	class Meta:
		ordering = ('-created',)
	
	def __str__(self):
		return f'{self.name} {self.created:%Y %b %d %H:%M}'


class OrderItemManager(models.Manager):
	
	def get_queryset(self):
		return super().get_queryset().filter(product__is_active=True)
	
class OrderItem(models.Model):
	order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
	product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
	price = models.DecimalField(max_digits=5, decimal_places=2)
	quantity = models.PositiveIntegerField(default=1)
	
	def __str__(self):
		return f'{self.product.title} - {self.order}'
	
	objects = models.Manager()
	products = OrderItemManager()
	
	