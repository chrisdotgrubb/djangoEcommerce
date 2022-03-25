from django. urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from user import views
from .forms import UserLoginForm

app_name = 'user'

urlpatterns = [
	path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', form_class=UserLoginForm), name='login'),
	path('logout/', auth_views.LogoutView.as_view(next_page='/user/login/'), name='logout'),
	path('register/', views.user_registration_view, name='register'),
	path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
	path('dashboard/', views.dashboard_view, name='dashboard'),
	path('profile/edit/', views.edit_profile_view, name='edit_profile'),
	path('profile/delete/', TemplateView.as_view(template_name='user/delete_confirm.html'), name='delete_confirm'),
	path('profile/delete/delete', views.delete_profile_view, name='delete_profile'),
	path('profile/delete_finished/', TemplateView.as_view(template_name='user/delete_finished.html'), name='delete_finished'),
]

htmx_urlpatterns = [
	path('check_username/', views.check_username, name="check_username"),
	path('check_email/', views.check_email, name="check_email"),
]

urlpatterns += htmx_urlpatterns
