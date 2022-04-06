from django.contrib import admin
from django.db.models import Count, F

from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ['name', 'slug', 'products_in_category']
	prepopulated_fields = {'slug': ('name',)}
	
	def get_queryset(self, request):
		qs = super().get_queryset(request)
		qs = qs.annotate(counter=Count('product'))
		return qs
		
	def products_in_category(self, obj):
		return obj.product.count()
	
	products_in_category.admin_order_field = 'counter'
	ordering = ('name',)

		
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = [
		'title',
		'pk',
		'author',
		'slug',
		'price',
		'in_stock',
		'is_active',
		'created',
		'updated',
	]
	list_filter = ('in_stock', 'is_active')
	list_editable = ('price', 'is_active')
	prepopulated_fields = {'slug': ('title',)}
	ordering = ('-is_active', '-created')
