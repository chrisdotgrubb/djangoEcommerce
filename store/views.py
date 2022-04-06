from django.contrib import messages
from django.db.models import Count
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from cart.forms import AddForm
from order.models import OrderItem
from .models import Category, Product


def products_index_view(request):
	popular = OrderItem.products.values('product').annotate(count=Count('product')).order_by('-count')[:5]
	products = Product.products.filter(id__in=popular.values('product'))
	
	context = {
		'products': products
	}
	return TemplateResponse(request, 'store/index.html', context)


def product_detail_view(request, slug):
	product = get_object_or_404(Product, slug=slug, in_stock=True)
	context = {
		'product': product,
		'form': AddForm,
	}
	return TemplateResponse(request, 'store/product_detail.html', context)


def category_view(request, slug):
	category = get_object_or_404(Category, slug=slug)
	products = Product.products.filter(category=category)
	context = {
		'category': category,
		'products': products,
	}
	return TemplateResponse(request, 'store/category.html', context)
