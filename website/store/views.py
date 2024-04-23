from datetime import timezone

from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from users.forms import AddressForm, PaymentForm
from store.models import StoreItem, OrderItem, Order


# Create your views here.
@login_required()
def add_to_cart(request, id):
    item = StoreItem.objects.get(pk=id)
    queryset = Order.objects.filter(status='pending', profile=request.user.user_profile)
    item_list = StoreItem.objects.all()
    if queryset:
        cart_item = OrderItem.objects.create(quantity=1, storeItem=item, order=queryset.first())
        messages.success(request, f"Successfully added {cart_item.quantity} item(s) to cart!")
        return render(request, 'store/listings.html', {'item_list': item_list})
    else:
        new_order = Order.objects.create(profile=request.user.user_profile, status='pending')
        cart_item = OrderItem.objects.create(quantity=1, storeItem=item, order=new_order)
        messages.success(request, f"Successfully added {cart_item.quantity} item(s) to cart!")
        return render(request, 'store/listings.html', {'item_list': item_list})


def home(request):
    template = loader.get_template('store/home.html')
    return render(request, 'store/home.html')

def browse(request):
    template = loader.get_template('store/listings.html')
    item_list = StoreItem.objects.all()
    return render(request, 'store/listings.html', {'item_list': item_list})


def item_detail(request, id):
    if request.method == 'GET':
        item = StoreItem.objects.get(pk=id)
        return render(request, 'store/item_detail.html', {'item': item})

@login_required()
def shopping_cart(request):
    queryset = Order.objects.filter(status='pending', profile=request.user.user_profile)
    order = queryset.first()
    cart_items = OrderItem.objects.filter(order=order)

    context = {
        'order': order,
        'cart_items':cart_items
    }
    return render(request, 'store/shopping_cart.html', context)

@login_required()
def remove_item(request, id):
    item = OrderItem.objects.get(pk=id)
    item.delete()
    return redirect(request.path)

@login_required()
def clear_cart(request):
    queryset = Order.objects.filter(status='pending', profile=request.user.user_profile)
    for item in queryset:
        item.delete()
    return redirect('store:shopping_cart')
@login_required()
def checkout(request):
    queryset = Order.objects.filter(status='pending', profile=request.user.user_profile)
    order = queryset.first()
    cart_items = OrderItem.objects.filter(order=order)

    if 'order' in locals() and 'cart_items' in locals():
        order.calculate_order()
        context = {
            'order': order,
            'cart_items': cart_items
        }
        return render(request, 'store/checkout.html', context)
    else:
        return redirect('store:shopping_cart')
@login_required()
def place_order(request):
    form = PaymentForm(request.POST or None)
    if form.is_valid():
        order = Order.objects.filter(status='pending', profile=request.user.user_profile)
        order.status = 'complete'
        order.orderDate = timezone.now()
        messages.success(request, f"Order has been placed! Go to Order History to review your order")
        return redirect('store:home')

    return render(request, 'store/place_order.html', {'form':form})
