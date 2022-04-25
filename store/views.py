from django.contrib import messages
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404
from cart.forms import AddForm
from .models import Category, Product


#TODO add popular products
def products_index_view(request):
	products = Product.objects.prefetch_related('product_image').filter(is_active=True)
	
	context = {
		'products': products
	}
	return TemplateResponse(request, 'store/index.html', context)


def product_detail_view(request, slug):
	product = get_object_or_404(Product, slug=slug, is_active=True)
	in_wish = False
	if product.users_wishlist.filter(id=request.user.id).exists():
		in_wish = True
	context = {
		'product': product,
		'form': AddForm,
		'in_wish': in_wish
	}
	return TemplateResponse(request, 'store/product_detail.html', context)


def category_view(request, slug):
	category = get_object_or_404(Category, slug=slug)
	products = Product.objects.filter(category__in=Category.objects.filter(slug=slug).get_descendants(include_self=True))
	context = {
		'category': category,
		'products': products,
	}
	return TemplateResponse(request, 'store/category.html', context)
