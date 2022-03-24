from django.contrib import messages
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from cart.forms import AddForm
from .models import Category, Product


def products_all_view(request):
	products = Product.products.all()
	context = {
		'products': products,
	}
	return TemplateResponse(request, 'home.html', context)


def product_detail_view(request, slug):
	product = get_object_or_404(Product, slug=slug, in_stock=True)
	context = {
		'product': product,
		'form': AddForm,
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
