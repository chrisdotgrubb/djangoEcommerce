from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, Product, ProductImage, ProductSpecification, ProductSpecificationValue, ProductType


class CategoryAdmin(MPTTModelAdmin):
	fields = (
		'name',
		'slug',
		'parent',
		'is_active'
	)
	readonly_fields = ('slug',)


class ProductSpecificationInline(admin.TabularInline):
	model = ProductSpecification


class ProductImageInline(admin.TabularInline):
	model = ProductImage


class ProductSpecificationValueInline(admin.TabularInline):
	model = ProductSpecificationValue


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
	inlines = [
		ProductSpecificationInline,
	]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	readonly_fields = ('slug',)
	inlines = [
		ProductSpecificationValueInline,
		ProductImageInline,
	]


admin.site.register(Category, CategoryAdmin)
