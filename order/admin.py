from django.contrib import admin
from django.db.models import F
from .models import Order, OrderItem


class StatesWithOrders(admin.SimpleListFilter):
	title = 'State'
	parameter_name = 'state'
	
	def lookups(self, request, model_admin):
		qs = set(Order.objects.values_list('state', flat=True))
		query = []
		for state in sorted(qs):
			query.append((state, state))
		return query

	def queryset(self, request, queryset):
		if self.value():
			return queryset.filter(state=self.value())
		return queryset
	
	
class OrderAdmin(admin.ModelAdmin):
	list_display = ('name', 'state', 'created', 'total_paid', 'is_paid')
	fields = (
		'user',
		'name',
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
	list_filter = ('is_paid', StatesWithOrders, 'name')
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
	list_filter = ('quantity', 'product')
	ordering = ('order', '-quantity')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)
