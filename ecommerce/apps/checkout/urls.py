from django.urls import path
from . import views

app_name = 'checkout'

urlpatterns = [
	path('delivery_choices/', views.delivery_choices_view, name='delivery_choices'),
	path('delivery_address/', views.delivery_address_view, name='delivery_address'),
	path('payment_selection/', views.payment_selection_view, name='payment_selection'),
	path('payment_complete/', views.payment_complete_view, name='payment_complete'),
	path('payment_success/', views.payment_success_view, name='payment_success'),
	path('update_delivery/<int:delivery_id>/', views.update_delivery, name='update_delivery')
]
