from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django_htmx.http import trigger_client_event
from cart.cart import Cart
from cart.forms import QuantityForm
from store.models import Product


def cart_view(request):
	cart = Cart(request)
	context = {
		'cart': cart,
	}
	return TemplateResponse(request, 'store/cart/cart.html', context)


def cart_add(request, product_id):
	product_qty = request.POST.get('qty', 0)
	cart = Cart(request)
	cart.add(product_id, product_qty)
	
	product = get_object_or_404(Product, id=product_id, in_stock=True)
	context = {
		'product': product,
		'form': QuantityForm,
	}
	
	response = TemplateResponse(request, 'store/cart/_form.html', context)
	trigger_client_event(response, 'cartUpdatedEvent', {}, )
	
	return response


def cart_remove(request):
	pass


def cart_update_number(request):
	return TemplateResponse(request, 'store/cart/_total.html')


def cart_update_details(request):
	return TemplateResponse(request, 'store/cart/_details.html')


def cart_update_footer(request):
	return TemplateResponse(request, 'store/cart/_footer.html')



