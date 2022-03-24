from django. urls import path
from user import views

app_name = 'user'

urlpatterns = [
	path('register/', views.user_registration_view, name='register'),
	path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
	path('dashboard/', views.dashboard_view, name='dashboard')
]
