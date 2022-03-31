from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.template.response import TemplateResponse


@login_required
def CartView(request):
	return TemplateResponse(request, 'payment/payment.html')

