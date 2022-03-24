from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .forms import RegistrationForm
from .token import account_activation_token


def user_registration_view(request):
	
	if request.user.is_authenticated:
		return redirect('/')
	
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save(commit=False)
			user.email = form.cleaned_data['email']
			user.set_password(form.cleaned_data['password'])
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
	else:
		form = RegistrationForm()
		context = {
			'form': form
		}
		return TemplateResponse(request, 'registration/register.html', context=context)
