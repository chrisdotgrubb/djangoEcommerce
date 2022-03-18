from django.shortcuts import render
from django.template.response import TemplateResponse


def cart_view(request):
	return TemplateResponse(request, 'store/cart.html')
