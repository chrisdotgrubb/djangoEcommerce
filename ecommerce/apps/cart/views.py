from decimal import Decimal

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from django_htmx.http import trigger_client_event
from ecommerce.apps.cart.cart import Cart
from ecommerce.apps.cart.forms import AddForm, QuantityForm
from ecommerce.apps.store.models import Product


def cart_view(request):
	cart = Cart(request)
	
	form = QuantityForm(initial={'qty': 1})
	context = {
		'cart': cart,
		'form': form,
	}
	
	product_ids = cart.cart.keys()
	products = Product.objects.filter(id__in=product_ids)
	cart = cart.cart
	
	for product in products:
		cart[str(product.id)]['product'] = product
	
	return TemplateResponse(request, 'cart/cart.html', context)


@require_http_methods(["POST"])
def cart_add(request, product_id):
	product_qty = request.POST.get('qty', 0)
	cart = Cart(request)
	cart.add(product_id, product_qty)
	
	product = get_object_or_404(Product, id=product_id, is_active=True)
	context = {
		'product': product,
		'form': AddForm,
	}
	
	response = TemplateResponse(request, 'cart/_add.html', context)
	trigger_client_event(response, 'cartUpdatedEvent', {}, )
	
	return response


@require_http_methods(["DELETE"])
def cart_delete(request, product_id):
	cart = Cart(request)
	cart.delete(product_id)
	
	response = HttpResponse()
	trigger_client_event(response, 'cartUpdatedEvent', {}, )
	
	return response


@require_http_methods(["POST"])
def cart_choose_quantity(request, product_id):
	product_qty = request.POST.get('qty', 0)
	cart = Cart(request)
	cart.set_quantity(product_id, product_qty)
	form = QuantityForm(initial={'qty': product_qty})
	
	product = get_object_or_404(Product, id=product_id, is_active=True)
	context = {
		'product': product,
		'form': form,
	}
	
	response = TemplateResponse(request, 'cart/_quantity.html', context)
	trigger_client_event(response, 'cartUpdatedEvent', {}, )
	if product_qty == '0':
		trigger_client_event(response, f'deletedEvent-{product_id}', {})
	
	return response


def cart_update_number(request):
	return TemplateResponse(request, 'cart/_total.html')


def cart_update_details(request):
	return TemplateResponse(request, 'cart/_details.html')


def cart_update_footer(request):
	return TemplateResponse(request, 'cart/_footer.html')


def cart_update_item_total(request, product_id):
	product_ids = request.session['cart'].keys()
	products = Product.objects.filter(id__in=product_ids)
	cart = request.session['cart'].copy()
	
	for product in products:
		cart[str(product.id)]['product'] = product
		cart[str(product.id)]['price'] = product.regular_price
	
	for item in cart.values():
		item['price'] = Decimal(item['price'])
		item['total_price'] = item['price'] * item['qty']
	
	context = {
		'cart': cart,
		'products': products
	}
	pid = str(product_id)
	if pid in cart:
		item = cart[pid]
		context['item'] = item
	
	return TemplateResponse(request, 'cart/_item_total.html', context)

#TODO add shipping options
