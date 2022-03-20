from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
	path('', views.cart_view, name='cart'),
	path('add/<int:product_id>/', views.cart_add, name='add'),
	path('update/total/', views.cart_update_number, name='update_total'),
	path('update/details/', views.cart_update_details, name='update_details'),
	path('update/footer/', views.cart_update_footer, name='update_footer'),
]
