from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
	path('', views.cart_view, name='cart'),
	path('add/<int:product_id>/', views.cart_add, name='add'),
	path('chooseqty/<int:product_id>/', views.cart_choose_quantity, name='choose_qty'),
	path('update/item_total/<int:product_id>/', views.cart_update_item_total, name='update_item_total'),
	path('update/total/', views.cart_update_number, name='update_total'),
	path('update/details/', views.cart_update_details, name='update_details'),
	path('update/footer/', views.cart_update_footer, name='update_footer'),
]
