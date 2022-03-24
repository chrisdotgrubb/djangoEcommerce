from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .forms import RegistrationForm
from .models import MyUser
from .token import account_activation_token


def user_registration_view(request):
	if request.user.is_authenticated:
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
	except:
		return TemplateResponse(request, 'registration/activation_invalid.html')
	
	if user is not None and account_activation_token.check_token(user, token):
		user.is_active = True
		user.save()
		login(request, user)
		return redirect('user:dashboard')
	else:
		return TemplateResponse(request, 'registration/activation_invalid.html')


@login_required
def dashboard_view(request):
	return TemplateResponse(request, 'user/dashboard.html')
