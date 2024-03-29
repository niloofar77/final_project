from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from .models import User, Profile,FAQ
from django.contrib.auth.models import Group


class UserAdmin(BaseUserAdmin):
	form = UserChangeForm
	add_form = UserCreationForm
	list_display = ('full_name', 'email', 'is_admin')
	list_filter = ('is_admin',)
	fieldsets = (
		('Main', {'fields':('full_name', 'email', 'password')}),
		('Personal info', {'fields':('is_active',)}),
		('Permissions', {'fields':('is_admin',)})
	)
	add_fieldsets = (
		(None, {
			'fields':('full_name', 'email', 'password1', 'password2')
		}),
	)
	search_fields = ('email',)
	ordering = ('email',)
	filter_horizontal = ()
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'answer','ordernumber','status']
    list_filter = ['status']

admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
admin.site.register(Profile)
admin.site.register(FAQ,FAQAdmin)
