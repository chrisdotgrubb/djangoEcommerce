import re
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, get_object_or_404
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from .forms import RegistrationForm, UserEditForm, UserAddressForm
from .models import MyUser, Address
from .token import account_activation_token
from ecommerce.apps.order.models import Order
from ecommerce.apps.store.models import Product
from django_htmx.http import trigger_client_event


def user_registration_view(request):
	if request.user.is_authenticated:
		messages.add_message(request, messages.INFO, 'You are already logged in. Log out if you want to create another account.')
		return redirect('/')
	
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.email = form.cleaned_data['email']
			user.set_password(form.cleaned_data['password2'])
			user.is_active = False
			user.save()
			
			current_site = get_current_site(request)
			subject = 'Activate your Account'
			message = render_to_string('registration/account_activation_email.html', {
				'user': user,
				'domain': current_site.domain,
				'uid': urlsafe_base64_encode(force_bytes(user.pk)),
				'token': account_activation_token.make_token(user),
			})
			user.email_user(subject=subject, message=message)
			messages.add_message(request, messages.SUCCESS, 'Account created, check your email to confirm activation.')
			return redirect('/')
		#TODO else:
	else:
		form = RegistrationForm()
	
	context = {
		'form': form
	}
	return TemplateResponse(request, 'registration/register.html', context=context)


def account_activate(request, uidb64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = get_object_or_404(MyUser, pk=uid)
	except ValueError:
		messages.add_message(request, messages.ERROR, 'Account error, may have already been activated.')
		return TemplateResponse(request, 'registration/activation_invalid.html')
	
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		messages.add_message(request, messages.SUCCESS, 'Email confirmed, your account is now active.')
		return redirect('user:dashboard')
	else:
		messages.add_message(request, messages.ERROR, 'Account error, may have already been activated.')
		return TemplateResponse(request, 'registration/activation_invalid.html')


@login_required
def dashboard_view(request):
	context = {}
	return TemplateResponse(request, 'user/dashboard.html', context)


@login_required
def edit_profile_view(request):
	if request.method == 'POST':
		form = UserEditForm(instance=request.user, data=request.POST)
		if form.is_valid():
			form.save()
			messages.add_message(request, messages.SUCCESS, 'Profile updated.')
		else:
			messages.add_message(request, messages.WARNING, 'Profile update failed.')
	else:
		form = UserEditForm(instance=request.user)
	context = {
		'form': form,
	}
	
	return TemplateResponse(request, 'user/edit_profile.html', context)


@login_required
def delete_profile_view(request):
	user = get_object_or_404(MyUser.active, username=request.user)
	user.is_active = False
	user.save()
	logout(request)
	return redirect('user:delete_finished')


def check_username(request):
	username = request.POST.get('username')
	if username:
		if len(username) < 4:
			return HttpResponse('<div id="username-error" style="color:red" class="mb-1 ps-2">Username too short</div>')
		elif MyUser.active.filter(username__iexact=username).exists():
			return HttpResponse('<div id="username-error" style="color:red" class="mb-1 ps-2">Username taken</div>')
		elif MyUser.inactive.filter(username__iexact=username).exists():
			return HttpResponse('<div id="username-error" style="color:red" class="mb-1 ps-2">Account with this username may have been recently deleted</div>')
		else:
			return HttpResponse('<div id="username-error" style="color:green" class="mb-1 ps-2">Username available</div>')
	else:
		return HttpResponse('<div id="username-error" class="mb-1 ps-2">&nbsp;</div>')


def check_email(request):
	email = request.POST.get('email')
	pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
	if email:
		if not re.fullmatch(pattern, email):
			return HttpResponse('<div id="email-error" style="color:red" class="mb-1 ps-2">Email not valid</div>')
		elif MyUser.active.filter(email__iexact=email).exists():
			return HttpResponse('<div id="email-error" style="color:red" class="mb-1 ps-2">Email taken</div>')
		elif MyUser.inactive.filter(email__iexact=email).exists():
			return HttpResponse('<div id="email-error" style="color:red" class="mb-1 ps-2">Account with this email may have been recently deleted</div>')
		else:
			return HttpResponse('<div id="email-error" style="color:green" class="mb-1 ps-2">Email available</div>')
	else:
		return HttpResponse('<div id="email-error" class="mb-1 ps-2">&nbsp;</div>')


@login_required
def address_list_view(request):
	addresses = Address.objects.filter(customer=request.user)
	context = {
		'addresses': addresses,
	}
	return TemplateResponse(request, 'user/address/list.html', context)


@login_required
def address_form(request):
	context = {'form': UserAddressForm()}
	return TemplateResponse(request, 'user/address/_address_form.html', context)


@login_required
def get_address(request, uuid):
	address = Address.objects.get(pk=uuid)
	
	response = TemplateResponse(request, 'user/address/_address.html', {'address': address})
	trigger_client_event(response, 'addressAddedEvent', {}, )
	return response


@require_http_methods(["POST"])
@login_required
def add_address(request):
	form = UserAddressForm(request.POST)
	if form.is_valid():
		address = form.save(commit=False)
		address.customer = request.user
		address.save()
		return redirect(reverse('user:get_address', args=[address.pk]))


@login_required
def new_address_btn(request):
	return TemplateResponse(request, 'user/address/_new_address_btn.html')


@login_required
def edit_address_view(request, uuid):
	address = Address.objects.get(pk=uuid, customer=request.user)
	
	if request.method == 'POST':
		form = UserAddressForm(instance=address, data=request.POST)
		if form.is_valid():
			form.save()
			return HttpResponseRedirect(reverse('user:addresses'))
		else:
			return redirect('/')
	else:
		form = UserAddressForm(instance=address)
		context = {'form': form}
		return TemplateResponse(request, 'user/address/edit.html', context)


@login_required
def delete_address(request, uuid):
	Address.objects.get(pk=uuid, customer=request.user).delete()
	return HttpResponse()

@login_required
def set_default_address_view(request, uuid):
	Address.objects.filter(customer=request.user, default=True).update(default=False)
	Address.objects.filter(pk=uuid, customer=request.user).update(default=True)
	return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def add_to_wishlist_view(request, pk):
	product = get_object_or_404(Product, id=pk)
	if product.users_wishlist.filter(id=request.user.id).exists():
		product.users_wishlist.remove(request.user)
		messages.success(request, f'Removed {product.title} from your wishlist.')
	else:
		product.users_wishlist.add(request.user)
		messages.success(request, f'Added {product.title} to your wishlist.')
	return HttpResponseRedirect(request.META["HTTP_REFERER"])


@login_required
def wishlist_view(request):
	wishlist = Product.objects.filter(users_wishlist=request.user)
	context = {'wishlist': wishlist}
	return TemplateResponse(request, 'user/user_wish_list.html', context)

@login_required
def orders_view(request):
	orders = Order.objects.filter(user=request.user).filter(is_paid=True)
	context = {'orders': orders}
	return TemplateResponse(request, 'user/orders.html', context)
