
from django.urls import path, include
from . import views as store_views
from django.contrib.auth import views as auth_views

app_name = 'store'
urlpatterns = [
    path('', store_views.home, name='home'),
    path('browse/', store_views.browse, name='browse'),
    path('add/<int:id>', store_views.add_to_cart, name='add_to_cart'),
    path('item_detail/<int:id>', store_views.item_detail, name='item_detail'),
    path('cart/', store_views.shopping_cart, name='shopping_cart'),
    path('cart/remove_item/<int:id>', store_views.remove_item, name='remove_item'),
    path('cart/clear/', store_views.clear_cart, name='clear_cart'),
    path('cart/checkout/', store_views.checkout, name='checkout'),
    path('cart/place_order/<int:id>/<str:address>', store_views.place_order, name='place_order'),
    path('cart/payment_form', store_views.payment_form, name='payment_form'),
    path('cart/review_order', store_views.review_order, name='review_order')
]
