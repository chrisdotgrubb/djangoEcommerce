from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
	path('', views.products_index_view, name='products_all'),
	path('<slug:slug>/', views.product_detail_view, name='product_detail'),
	path('shop/<slug:slug>/', views.category_view, name='category'),
]

