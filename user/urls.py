from django.urls import path, reverse, reverse_lazy
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

from user import views
from .forms import UserLoginForm, PwdResetForm, SetPwdForm, PwdChangeForm

app_name = 'user'

urlpatterns = [
	path('login/', auth_views.LoginView.as_view(template_name='registration/login.html', form_class=UserLoginForm), name='login'),
	path('logout/', auth_views.LogoutView.as_view(next_page='/user/login/'), name='logout'),
	path('register/', views.user_registration_view, name='register'),
	path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
	path('password_reset/', auth_views.PasswordResetView.as_view(form_class=PwdResetForm, success_url=reverse_lazy('user:password_reset_done')), name='password_reset'),
	path('password_reset_confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
		form_class=SetPwdForm, success_url=reverse_lazy('user:password_reset_complete')), name='password_reset_confirm'),
	path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
	path('password_reset_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
	path('password_change/', auth_views.PasswordChangeView.as_view(
		form_class=PwdChangeForm, success_url=reverse_lazy('user:password_change_done')), name='password_change'),
	path('password_change_done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
	
	path('dashboard/', views.dashboard_view, name='dashboard'),
	path('profile/edit/', views.edit_profile_view, name='edit_profile'),
	path('profile/delete/', TemplateView.as_view(template_name='user/delete_confirm.html'), name='delete_confirm'),
	path('profile/delete/delete', views.delete_profile_view, name='delete_profile'),
	path('profile/delete_finished/', TemplateView.as_view(template_name='user/delete_finished.html'), name='delete_finished'),
	path('addresses/', views.address_list_view, name='addresses'),
	path('add_address/', views.add_address_view, name='add_address'),
	path('addresses/edit/<slug:id>/', views.edit_address_view, name='edit_address'),
	path('addresses/delete/<slug:id>/', views.delete_address_view, name='delete_address'),
	path('addresses/set_default/<slug:id>/', views.set_default_address_view, name='set_default_address'),
	path('wishlist/add_to_wishlist/<int:id>/', views.add_to_wishlist_view, name='add_to_wishlist'),
	path('wishlist/', views.wishlist_view, name='wishlist')
]

htmx_urlpatterns = [
	path('check_username/', views.check_username, name="check_username"),
	path('check_email/', views.check_email, name="check_email"),
]

urlpatterns += htmx_urlpatterns
