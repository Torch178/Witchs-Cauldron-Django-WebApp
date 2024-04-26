
from django.urls import path, include
from . import views as user_views
from django.contrib.auth import views as auth_views

app_name = 'users'
urlpatterns = [
    path('register/', user_views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('', user_views.profile, name='profile'),
    path('address_page/', user_views.address_page, name='address_page'),
    path('address_page/new_address/', user_views.new_address, name='new_address'),
    path('address_page/edit_address/<int:id>', user_views.edit_address, name='edit_address'),
    path('address_page/delete_address/<int:id>', user_views.delete_address, name='delete_address'),
    path('address_page/set_default_address/<int:id>', user_views.set_default_address, name='set_default_address'),
    path('profile_page/', user_views.profile_page, name='profile_page'),
    path('profile_page/edit_profile/', user_views.edit_profile, name='edit_profile'),
    path('profile_page/delete_profile/', user_views.delete_profile, name='delete_profile'),
    path('order_history/', user_views.order_history, name='order_history')
]
