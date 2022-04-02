from django.shortcuts import render
from django.http.response import JsonResponse
from cart.cart import Cart
from .models import Order, OrderItem

def add(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		user_id = request.user.id
		order_key = request.POST.get('order_key')
		cart_total = cart.get_total_price()
		
		if Order.objects.filter(order_key=order_key).exists():
			pass
		else:
			order = Order.objects.create(user_id=user_id, name='name', address1='add1', address2='add2', total_paid=cart_total, order_key=order_key)  # need to replace this data
			order_id = order.pk
			for item in cart:
				OrderItem.objects.create(order_id=order_id, product=item['product'], price=item['price'], quantity=item['qty'])
				
	response = JsonResponse({'success': 'returned value'})
	return response


def payment_confirmation(data):
	Order.objects.filter(order_key=data).update(is_paid=True)
