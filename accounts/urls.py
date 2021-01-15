from django.urls import path
from . import views


app_name = 'accounts'
urlpatterns = [
	path('login/', views.user_login, name='login'),
	path('logout/', views.user_logout, name='logout'),
	path('register/', views.user_register, name='register'),
    path('edit_profile/<int:user_id>/', views.edit_profile, name='edit_profile'),
    path('profile/<int:pk>', views.view_profile, name='view_profile_with_pk'),
	path('my_account',views.show_account,name='my_account')

]