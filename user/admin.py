from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import RegistrationForm
from .models import MyUser

class MyUserAdmin(UserAdmin):
	list_display = ('username',	'first', 'email', 'created', 'is_staff', 'is_superuser', 'is_active')
	fieldsets = (
		(None, {'fields': ('username', 'email', 'first', 'phone', 'about')}),
		('Address', {'fields': ('address_line_1', 'address_line_2', 'town_city', 'country')}),
		('Perms', {'fields': ('is_staff', 'is_superuser', 'is_active')}),
		('Times', {'fields': ('created', 'updated')})
	)
	readonly_fields = ('created', 'updated')
	add_form = RegistrationForm
	add_fieldsets = ((None, {'fields':('username', 'email', 'password1', 'password2')}),('Permissions', {'fields':('is_active', 'is_staff', 'is_superuser')}))
	ordering = ('-created',)

admin.site.register(MyUser, MyUserAdmin)
