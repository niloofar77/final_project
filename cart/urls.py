from django.urls import path
from . import views


app_name = 'cart'
urlpatterns = [
	path('', views.detail, name='detail'),
	path('add/<int:product_id>/', views.cart_add, name='cart_add'),
	path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
	path('bookmark_add/<int:product_id>/', views.bookmark_add, name='bookmark_add'),
	path('bookmark_remove/<int:product.id>/', views.bookmark_remove, name='bookmark_remove'),
	# path('search/<str:your_search_query>', views.search_view, name='search_view'),
	path('search/', views.search, name='search'),
	path('contact/',views.contact,name='contact'),
	path('show/',views.show_cart,name='show'),
	path('about/',views.about,name='about'),

]