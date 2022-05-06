import logging

from django.contrib import messages
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required

from cart.cart import Cart
from .models import DeliveryOptions


@login_required
def delivery_choices_view(request):
	delivery_options = DeliveryOptions.objects.filter(is_active=True)
	context = {'delivery_options': delivery_options}
	
	try:
		if request.session['purchase']['delivery_id']:
			cart = Cart(request)
			delivery_type = DeliveryOptions.objects.get(id=request.session['purchase']['delivery_id'])
			updated_total_price = cart.get_grand_total(delivery_type.delivery_price)
			context['total'] = updated_total_price
			context['delivery_price'] = delivery_type.delivery_price
	except KeyError:
		pass
		
	return TemplateResponse(request, 'checkout/delivery_choices.html', context)
	

@login_required
def delivery_address_view(request):
	session = request.session
	if 'purchase' not in session:
		messages.info(request, 'Please select a delivery option')
		return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def payment_selection_view(request):
	pass


@login_required
def payment_complete_view(request):
	pass


@login_required
def payment_success_view(request):
	pass

@login_required
def update_delivery(request, delivery_id):
	cart = Cart(request)
	
	delivery_type = DeliveryOptions.objects.get(id=delivery_id)
	updated_total_price = cart.get_grand_total(delivery_type.delivery_price)
	
	session = request.session
	if 'purchase' not in session:
		session['purchase'] = {'delivery_id': delivery_id, 'delivery_name': delivery_type.delivery_name}
	else:
		session['purchase']['delivery_id'] = delivery_id
		session['purchase']['delivery_name'] = delivery_type.delivery_name
		session.modified = True
	
	response = TemplateResponse(request, 'checkout/_price.html', {'total': updated_total_price, 'delivery_price': delivery_type.delivery_price})
	return response
