from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
	path('', views.all_products_view, name='all_products'),
	path('item/<slug:slug>/', views.product_detail_view, name='product_detail'),
	path('search/<slug:slug>/', views.category_view, name='category'),
]

