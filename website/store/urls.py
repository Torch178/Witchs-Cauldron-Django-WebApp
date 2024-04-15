
from django.urls import path, include
from . import views as store_views
from django.contrib.auth import views as auth_views

app_name = 'store'
urlpatterns = [
    path('', store_views.home, name='home'),
    path('browse/', store_views.browse, name='browse'),
    path('add/<int:id>', store_views.add_to_cart, name='add_to_cart')
]
