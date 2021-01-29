from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'
urlpatterns = [
	path('login/', views.user_login, name='login'),
	path('logout/', views.user_logout, name='logout'),
	path('register/', views.user_register, name='register'),
    path('edit_profile/', views.edit_profile, name='edit_profile1'),
    path('profile/', views.view_profile, name='view_profile_with_pk'),
	path('my_account',views.show_account,name='my_account'),
	path('contact/',views.contact,name='contact'),
	path('password/', views.user_password, name='user_password'),
	path('faq/', views.faq, name='faq'),


]