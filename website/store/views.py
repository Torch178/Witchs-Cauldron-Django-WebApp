from datetime import timezone, datetime

from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from users.forms import AddressForm, PaymentForm
from store.models import StoreItem, OrderItem, Order
from users.models import Address
from django.db.models import Q


# Create your views here.
def home(request):
    template = loader.get_template('store/home.html')
    return render(request, 'store/home.html')

def browse(request):
    item_list = StoreItem.objects.all()
    search_criteria = request.GET.get('search_criteria')
    if search_criteria != '' and search_criteria is not None:
        item_list = item_list.filter(Q(name__icontains=search_criteria)
                                     | Q(description__icontains=search_criteria)
                                     | Q(manufacturer__icontains=search_criteria))
    else:
        search_criteria = ''
    page = request.GET.get('page')
    paginator = Paginator(item_list, 3)
    item_list = paginator.get_page(page)
    return render(request, 'store/listings.html', {'item_list': item_list,
                                                   'page': page, 'search_criteria': search_criteria})


def item_detail(request, id):
    if request.method == 'GET':
        item = StoreItem.objects.get(pk=id)
        return render(request, 'store/item_detail.html', {'item': item})

@login_required()
def shopping_cart(request):
    queryset = Order.objects.filter(status='pending', profile=request.user.user_profile)
    order = queryset.first()
    cart_items = OrderItem.objects.filter(order=order)
    if order is not None:
        order.calcualte_subtotal()
    context = {
        'order': order,
        'cart_items':cart_items
    }
    return render(request, 'store/shopping_cart.html', context)

@login_required()
def add_to_cart(request, id):
    item_exists = False
    new_item = StoreItem.objects.get(pk=id)
    queryset = Order.objects.filter(status='pending', profile=request.user.user_profile)
    item_list = StoreItem.objects.all()
    if queryset:
        order = queryset.first()
        order_list = OrderItem.objects.filter(order=order)
        for existing_item in order_list:
            if existing_item.storeItem == new_item:
                item_exists = True
                added_quantity = 1
                existing_item.quantity += added_quantity
                existing_item.save()
                messages.success(request, f"Successfully added {added_quantity} more {existing_item.storeItem.name} item(s) to cart!")
        if item_exists is False:
            cart_item = OrderItem.objects.create(quantity=1, storeItem=new_item, order=order)
            messages.success(request, f"Successfully added {cart_item.quantity} item(s) to cart!")
        return redirect('store:browse')
    else:
        new_order = Order.objects.create(profile=request.user.user_profile, status='pending')
        cart_item = OrderItem.objects.create(quantity=1, storeItem=new_item, order=new_order)
        messages.success(request, f"Successfully added {cart_item.quantity} item(s) to cart!")
        return redirect('store:browse')

@login_required()
def remove_item(request, id):
    item = OrderItem.objects.get(id=id)
    item.delete()
    return redirect('store:shopping_cart')

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
    addresses = Address.objects.filter(profile=request.user.user_profile)
    if addresses.count() == 0:
        messages.error(request, "No addresses found on file, please add an address for shipping.")
        return redirect('users:new_address')
    if 'order' in locals() and 'cart_items' in locals():
        order.calculate_order()
        order.save()
        address = Address.objects.filter(profile=request.user.user_profile, default_address=True).first()
        context = {
            'order': order,
            'cart_items': cart_items,
            'address': address
        }
        return render(request, 'store/checkout.html', context)
    else:
        return redirect('store:shopping_cart')

@login_required()
def payment_form(request):
    form = PaymentForm(request.POST or None)
    if form.is_valid():
        get_card = form.cleaned_data['cardNumber']
        order = Order.objects.filter(profile=request.user.user_profile, status='pending').first()
        card = str(get_card)
        order.payMethod = ('************' + card[12:])
        order.save()
        return redirect('store:review_order')
    return render(request, 'store/payment_form.html', {'form':form})

@login_required()
def review_order(request):
    addresses = Address.objects.filter(profile=request.user.user_profile)
    if addresses.count() == 0:
        messages.error(request, "No addresses found on file, please add an address for shipping.")
        return redirect('users:new_address')
    address = Address.objects.filter(profile=request.user.user_profile, default_address=True).first()
    order = Order.objects.filter(profile=request.user.user_profile, status='pending').first()
    return render(request, 'store/review_order.html', {'order':order, 'address':address})

@login_required()
def place_order(request, id, address):
    order = Order.objects.get(pk=id)
    order.status = 'complete'
    order.shippingAddress = address
    order.orderDateTime = datetime.now()
    order.save()
    messages.success(request, 'Order placed!')
    return redirect('store:home')

#Christian Price Luke
#1234123412341234
#12/26
#123