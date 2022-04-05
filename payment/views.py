import json
import logging
import stripe
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.response import TemplateResponse
from django.views.decorators.csrf import csrf_exempt

from cart.cart import Cart
from order.views import payment_confirmation
from payment.forms import PaymentForm


@login_required
def CartView(request):
	cart = Cart(request)
	total = str(cart.get_total_price()).replace('.', '')
	total = int(total)

	stripe.api_key = 'sk_test_51KjPSyIu1jKvkROghajB8v3FL6yinPOO4Ni5baDLToV99GRp991EsHMtqJQsuvjF93QmyBx0NcOoLqZhI6JOvER500K2D6rPAU'
	intent = stripe.PaymentIntent.create(
		amount=total,
		currency='usd',
		metadata={'userid': request.user.id}
	)
	form = PaymentForm(use_required_attribute=False)
	content = {
		'client_secret': intent.client_secret,
		'form': form
	}
	
	return TemplateResponse(request, 'payment/payment.html', content)


@csrf_exempt
def stripe_webhook(request):
	payload = request.body
	event = None
	
	try:
		event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
	except ValueError as e:
		logging.debug(e)
		return HttpResponse(status=400)
	
	if event.type == 'payment_intent.succeeded':
		payment_confirmation(event.data.object.client_secret)
	else:
		logging.debug(f'Unhandled event type {event.type}')
	
	return HttpResponse(status=200)


def order_placed_view(request):
	cart = Cart(request)
	cart.clear()
	return TemplateResponse(request, 'payment/orderplaced.html')


