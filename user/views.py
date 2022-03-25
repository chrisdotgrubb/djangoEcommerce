import re

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import RegistrationForm, UserEditForm
from .models import MyUser
from .token import account_activation_token


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
	else:
		form = RegistrationForm()
	
	context = {
		'form': form
	}
	return TemplateResponse(request, 'registration/register.html', context=context)


def account_activate(request, uidb64, token):
	try:
		uid = force_str(urlsafe_base64_decode(uidb64))
		user = MyUser.objects.get(pk=uid)
	except ObjectDoesNotExist:
		messages.add_message(request, messages.ERROR, 'Account not found.')
		return TemplateResponse(request, 'registration/activation_invalid.html')
	
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		messages.add_message(request, messages.SUCCESS, 'Account activated, email confirmed.')
		return redirect('user:dashboard')
	else:
		messages.add_message(request, messages.ERROR, 'Account error, may have already been activated.')
		return TemplateResponse(request, 'registration/activation_invalid.html')


@login_required
def dashboard_view(request):
	return TemplateResponse(request, 'user/dashboard.html')


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
	user = MyUser.objects.get(username=request.user)
	user.is_active = False
	user.save()
	logout(request)
	return redirect('user:delete_finished')


def check_username(request):
	username = request.POST.get('username')
	if username:
		if len(username) < 4:
			return HttpResponse('<div id="username-error" style="color:red" class="mb-1 ps-2">Username too short</div>')
		elif MyUser.objects.filter(username__iexact=username).exists():
			return HttpResponse('<div id="username-error" style="color:red" class="mb-1 ps-2">Username taken</div>')
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
		if MyUser.objects.filter(email__iexact=email).exists():
			return HttpResponse('<div id="email-error" style="color:red" class="mb-1 ps-2">Email taken</div>')
		else:
			return HttpResponse('<div id="email-error" style="color:green" class="mb-1 ps-2">Email available</div>')
	else:
		return HttpResponse('<div id="email-error" class="mb-1 ps-2">&nbsp;</div>')
