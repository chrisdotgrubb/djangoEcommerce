from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from cart.cart import Cart
from store.models import Product


def cart_view(request):
	return TemplateResponse(request, 'store/cart.html')


def cart_add_view(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		product_id = int(request.POST.get('productid'))
		product = get_object_or_404(Product, id=product_id)
		cart.add(product=product)
		response = JsonResponse({'test': 'data'})
		return response
		
		