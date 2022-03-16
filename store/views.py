from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from .models import Category, Product





def all_products_view(request):
	products = Product.objects.all()
	context = {
		'products': products,
	}
	return TemplateResponse(request, 'store/home.html', context)


def product_detail_view(request, slug):
	product = get_object_or_404(Product, slug=slug, in_stock=True)
	context = {
		'product': product,
	}
	return TemplateResponse(request, 'store/product_detail.html', context)


def category_view(request, slug):
	category = get_object_or_404(Category, slug=slug)
	products = Product.objects.filter(category=category)
	context = {
		'category': category,
		'products': products,
	}
	return TemplateResponse(request, 'store/category.html', context)
