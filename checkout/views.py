import json
import logging

from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from paypalcheckoutsdk.orders import OrdersGetRequest

from cart.cart import Cart
from order.models import Order, OrderItem
from .models import DeliveryOptions
from user.models import Address
from .paypal import PayPalClient


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
		messages.info(request, 'Please select a delivery option.')
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	
	delivery_id = request.session['purchase']['delivery_id']
	delivery_obj = DeliveryOptions.objects.get(id=delivery_id)
	
	cart = Cart(request)
	addresses = Address.objects.filter(customer=request.user).order_by('-default')
	
	subtotal = cart.get_subtotal_price()
	tax = cart.get_tax_price()
	delivery_price = delivery_obj.delivery_price
	total = cart.get_grand_total(delivery_price=delivery_price)
	
	try:
		if 'address' not in request.session:
			session['address'] = {'address_id': str(addresses[0].id)}
		else:
			session['address']['address_id'] = str(addresses[0].id)
			session.modified = True
	except IndexError:
		messages.info(request, 'Please add an address for delivery, then checkout again.')
		return HttpResponseRedirect(reverse('user:addresses'))
		
	context = {
		'addresses': addresses,
		'subtotal': subtotal,
		'tax': tax,
		'delivery_price': delivery_price,
		'total': total,
	}
	return TemplateResponse(request, 'checkout/delivery_address.html', context)


@login_required
def payment_selection_view(request):
	session = request.session
	if 'address' not in session:  # shouldn't happen
		messages.info(request, 'Please select a delivery address')
		return HttpResponseRedirect(request.META['HTTP_REFERER'])
	
	delivery_id = request.session['purchase']['delivery_id']
	delivery_obj = DeliveryOptions.objects.get(id=delivery_id)
	cart = Cart(request)
	
	subtotal = cart.get_subtotal_price()
	tax = cart.get_tax_price()
	delivery_price = delivery_obj.delivery_price
	total = cart.get_grand_total(delivery_price=delivery_price)
	
	context = {
		'subtotal': subtotal,
		'tax': tax,
		'delivery_price': delivery_price,
		'total': total,
	}
	
	return TemplateResponse(request, 'checkout/payment_selection.html', context)


@login_required
def payment_complete_view(request):
	PPClient = PayPalClient()
	
	body = json.loads(request.body)
	data = body['orderID']
	
	request_order = OrdersGetRequest(data)
	response = PPClient.client.execute(request_order)
	
	purchase_units = response.result.purchase_units[0]
	
	cart = Cart(request)
	order = Order.objects.create(
		user=request.user,
		name=purchase_units.shipping.name.full_name,
		email=purchase_units.payee.email_address,
		address1=purchase_units.shipping.address.address_line_1,
		address2=purchase_units.shipping.address.address_line_2,
		city=purchase_units.shipping.address.admin_area_2,
		state=purchase_units.shipping.address.admin_area_1,
		country=purchase_units.shipping.address.country_code,
		zip_code=purchase_units.shipping.address.postal_code,
		total_paid=purchase_units.amount.value,
		order_key=response.result.id,
		payment_option='paypal',
		is_paid=True
	)
	order_id = order.pk
	for key, item in zip(cart.cart.keys(), cart):
		OrderItem.objects.create(order_id=order_id, product_id=key, price=item['price'], quantity=item['qty'])
		
	return JsonResponse('payment complete', safe=False)


@login_required
def payment_success_view(request):
	cart = Cart(request)
	cart.clear()
	return TemplateResponse(request, 'checkout/payment_success.html')


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
