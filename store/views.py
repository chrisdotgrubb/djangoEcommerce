from django.template.response import TemplateResponse
from .models import Category, Product





def all_products(request):
	products = Product.objects.all()
	context = {
		'products': products
	}
	return TemplateResponse(request, 'store/home.html', context)




