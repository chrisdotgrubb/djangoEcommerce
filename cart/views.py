import logging

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from cart.cart import Cart
from store.models import Product


def cart_view(request):
	return TemplateResponse(request, 'store/cart.html')


# def cart_add_view(request):
# 	cart = Cart(request)
# 	if request.POST.get('action') == 'post':
# 		product_id = int(request.POST.get('productid'))
# 		product_qty = int(request.POST.get('productqty'))
# 		product = get_object_or_404(Product, id=product_id)
# 		cart.add(product, product_qty)
# 		response = JsonResponse({'test': 'data'})
# 		return response
		

def cart_add(request, product_id):
	logging.debug(request.POST.get('qty', False))
	cart = Cart(request)
	cart.add(product_id)
	
	return TemplateResponse(request, 'store/cart_menu.html')




