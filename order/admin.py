from django.contrib import admin
from django.db.models import F
from .models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
	list_display = ('name', 'created', 'total_paid', 'is_paid')
	fields = (
		'user',
		'name',
		'phone',
		'address1',
		'address2',
		'city',
		'state',
		'country',
		'zip_code',
		'total_paid',
		'order_key',
		'is_paid',
		'created',
		'updated'
	)
	readonly_fields = ('user', 'created', 'updated', 'order_key')
	list_filter = ('is_paid', 'name', 'state')
	ordering = ('-created',)


class OrderItemAdmin(admin.ModelAdmin):
	list_display = ('order', 'product', 'price', 'quantity', 'total')
	fieldsets = (
		(None, {'fields': ('order',)}),
		('Item', {'fields': ('product', 'price', 'quantity', 'total')})
	)
	
	def has_change_permission(self, request, obj=None):
		return False
	
	def has_delete_permission(self, request, obj=None):
		return False
	
	def has_add_permission(self, request):
		return False
	
	def get_queryset(self, request):
		qs = super().get_queryset(request)
		qs = qs.annotate(total=(F('price') * F('quantity')))
		return qs
	
	def total(self, obj):
		return f'{obj.total:.2f}'
	
	total.admin_order_field = 'total'
	list_filter = ('quantity',)
	ordering = ('order', '-quantity')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
