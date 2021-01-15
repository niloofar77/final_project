from django.contrib import admin
from .models import Category, Product,Comment

admin.site.register(Comment)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
	list_display = ('name', 'slug')
	prepopulated_fields = {'slug':('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'available')
	list_filter = ('available', 'created')
	list_editable = ('price',)
	prepopulated_fields = {'slug':('name',)}
	raw_id_fields = ('category',)
	actions = ('make_available',)

	def make_available(self, request, queryset):
		rows = queryset.update(available=True)
		self.message_user(request, f'{rows} updated')
	make_available.short_description = 'make all available'
# @admin.register(Comment)
# class CommentAdmin(admin.ModelAdmin):
# #     list_display = ('name', 'body', 'product', 'created_on', 'active')
# #     list_filter = ('active', 'created_on')
# #     search_fields = ('name', 'email', 'body')
# #     actions = ['approve_comments']
# #
# #     def approve_comments(self, request, queryset):
# #         queryset.update(active=True)