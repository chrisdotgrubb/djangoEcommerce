from django.template.response import TemplateResponse
from django.contrib.auth.decorators import login_required
from .models import DeliveryOptions


@login_required
def delivery_choices_view(request):
	delivery_options = DeliveryOptions.objects.filter(is_active=True)
	context = {'delivery_options': delivery_options}
	return TemplateResponse(request, 'checkout/delivery_choices.html', context)


@login_required
def cart_update_delivery_view(request):
	pass


@login_required
def delivery_address_view(request):
	pass


@login_required
def payment_selection_view(request):
	pass


@login_required
def payment_complete_view(request):
	pass


@login_required
def payment_success_view(request):
	pass




