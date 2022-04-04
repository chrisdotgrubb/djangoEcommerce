from django.shortcuts import render
from django.http.response import JsonResponse
from cart.cart import Cart
from .models import Order, OrderItem


def add(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		user_id = request.user.id
		order_key = request.POST.get('order_key')
		form_data = request.POST
		cart_total = cart.get_total_price()
		
		if Order.objects.filter(order_key=order_key).exists():
			pass
		else:
			order = Order.objects.create(
				user_id=user_id,
				name=form_data['name'],
				phone=form_data['phone'],
				address1=form_data['address'],
				address2=form_data['address2'],
				city=form_data['city'],
				country=form_data['country'],
				state=form_data['state'],
				zip_code=form_data['zipcode'],
				total_paid=cart_total,
				order_key=order_key
			)
			order_id = order.pk
			for item in cart:
				OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])
	
	response = JsonResponse({'success': 'returned value'})
	return response


def payment_confirmation(data):
	Order.objects.filter(order_key=data).update(is_paid=True)


def user_orders(request):
	user_id = request.user.id
	orders = Order.objects.filter(user_id=user_id).filter(is_paid=True)
	return orders
