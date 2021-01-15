from django.urls import path
from . import views


app_name = 'shop'
urlpatterns = [
	path('', views.home, name='home'),
	path('category/<slug:slug>/', views.home, name='category_filter'),
	# path('<slug:slug>/<int:year>-<int:month>-<int:day>-', views.product_detail, name='product_detail'),
	path('<slug:slug>/', views.product_detail, name='product_detail'),

]