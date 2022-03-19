from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
	path('', views.cart_view, name='cart'),
	path('add/<int:product_id>/', views.cart_add, name='add'),
	path('update/total/', views.update_cart_number, name='update_total'),
]
