import logging

from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django_htmx.http import trigger_client_event
from cart.cart import Cart
from cart.forms import AddForm, QuantityForm
from store.models import Product


def cart_view(request):
	cart = Cart(request)
	context = {
		'cart': cart,
		'form': QuantityForm,
	}
	return TemplateResponse(request, 'store/cart/cart.html', context)


def cart_add(request, product_id):
	product_qty = request.POST.get('qty', 0)
	cart = Cart(request)
	cart.add(product_id, product_qty)
	
	product = get_object_or_404(Product, id=product_id, in_stock=True)
	context = {
		'product': product,
		'form': AddForm,
	}
	
	response = TemplateResponse(request, 'store/cart/_add.html', context)
	trigger_client_event(response, 'cartUpdatedEvent', {}, )
	
	return response


def cart_remove(request):
	pass


def cart_choose_quantity(request, product_id):
	product_qty = request.POST.get('qty', 0)
	cart = Cart(request)
	cart.set_quantity(product_id, product_qty)
	
	product = get_object_or_404(Product, id=product_id, in_stock=True)
	context = {
		'product': product,
		'form': QuantityForm,
	}
	
	response = TemplateResponse(request, 'store/cart/_quantity.html', context)
	trigger_client_event(response, 'cartUpdatedEvent', {}, )
	
	return response


def cart_update_number(request):
	return TemplateResponse(request, 'store/cart/_total.html')


def cart_update_details(request):
	return TemplateResponse(request, 'store/cart/_details.html')


def cart_update_footer(request):
	return TemplateResponse(request, 'store/cart/_footer.html')


def cart_update_item_total(request, product_id):
	cart = Cart(request).__iter__()
	logging.debug(cart)
	item = cart.cart[str(product_id)]
	context = {
		'cart': cart,
		'item': item,
	}
	
	return TemplateResponse(request, 'store/cart/_item_total.html', context)

