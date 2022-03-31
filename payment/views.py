import logging
import stripe
from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from cart.cart import Cart


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

	content = {
		'client_secret': intent.client_secret,
	}
	
	return TemplateResponse(request, 'payment/payment.html', content)
