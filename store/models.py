from django.db import models
from django.urls import reverse
from user.models import MyUser


class Category(models.Model):
	name = models.CharField(max_length=255, db_index=True)
	slug = models.SlugField(max_length=255, unique=True)
	
	class Meta:
		verbose_name_plural = 'Categories'
	
	def get_absolute_url(self):
		return reverse('store:category', args=[self.slug])
	
	def __str__(self):
		return self.name


class Product(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='product')
	created_by = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='product_creator')
	title = models.CharField(max_length=255)
	author = models.CharField(max_length=255, default='admin')
	description = models.TextField(blank=True)
	image = models.ImageField(upload_to='images/')
	slug = models.SlugField(max_length=255)
	price = models.DecimalField(max_digits=4, decimal_places=2)
	in_stock = models.BooleanField(default=True)
	is_active = models.BooleanField(default=True)
	created = models.DateTimeField(auto_now_add=True)
	updated = models.DateTimeField(auto_now=True)
	
	class Meta:
		verbose_name_plural = 'Products'
		ordering = ('-created',)
	
	def get_absolute_url(self):
		return reverse('store:product_detail', args=[self.slug])
		
	def __str__(self):
		return self.title
