from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from cart.cart import Cart
from cart.forms import QuantityForm
from store.models import Product


def cart_view(request):
	return TemplateResponse(request, 'store/cart.html')
		

def cart_add(request, product_id):
	product_qty = request.POST.get('qty', 0)
	cart = Cart(request)
	cart.add(product_id, product_qty)
	
	product = get_object_or_404(Product, id=product_id, in_stock=True)
	context = {
		'product': product,
		'form': QuantityForm,
	}
	
	return TemplateResponse(request, 'store/cart_form.html', context)




