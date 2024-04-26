from idlelib.history import History

from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages

from store.models import Order
from .forms import RegistrationForm, ProfileForm, AddressForm, UserForm
from django.contrib.auth.decorators import login_required
from .models import Profile, Address

# Create your views here.

def register(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f"Welcome {username}! You are registered.")
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required()
def profile(request):
    return render(request, 'users/profile.html')
@login_required()
def new_address(request):
    form = AddressForm(request.POST or None, initial={'profile': request.user.user_profile})
    if form.is_valid():
        form.save()
        queryset = Address.objects.filter(profile=request.user.user_profile)
        if queryset.count() == 1:
            address = queryset.first()
            address.default_address = True
            address.save()
        return redirect('users:address_page')
    return render(request, 'users/address_form.html', {'form': form})

def edit_address(request, id):
    address = Address.objects.get(id=id)
    form = AddressForm(request.POST or None, instance=address)
    if form.is_valid():
        form.save()
        return redirect('users:address_page')

    return render(request, 'users/address_form.html', {'form': form, 'address': address})

def delete_address(request, id):
    address = Address.objects.get(id=id)

    if request.method == 'POST':
        if address.default_address:
            new_default = Address.objects.filter(profile=request.user.user_profile).exclude(id=id).first()
            if new_default is not None:
                new_default.default_address = True
                new_default.save()
        address.delete()
        return redirect('users:address_page')
    return render(request, 'users/delete_address.html', {'address': address})

def set_default_address(request, id):
    address = Address.objects.get(id=id)
    address.default_address = True
    address.save()
    queryset = Address.objects.filter(profile=request.user.user_profile, default_address=True).exclude(id=id)
    for address in queryset:
        address.default_address = False
        address.save()
    return redirect('users:address_page')

def address_page(request):
    address_list = Address.objects.filter(profile=request.user.user_profile)
    return render(request, 'users/address_page.html', {'address_list': address_list})

def profile_page(request):
    return render(request, 'users/profile_page.html')

def edit_profile(request):
    user_form = UserForm(request.POST or None, instance=request.user)
    profile_form = ProfileForm(request.POST or None, instance=request.user.user_profile)
    if user_form.is_valid() and profile_form.is_valid():
        user_form.save()
        profile_form.save()
        return redirect('users:profile_page')

    return render(request, 'users/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})

def delete_profile(request):
    if request.method == 'POST':
        request.user.delete()
        messages.success(request, 'Profile deleted!')
        return redirect('store:home')
    return render(request, 'users/delete_profile.html')

def order_history(request):
    orders = Order.objects.filter(profile=request.user.user_profile).exclude(status='pending')

    return render(request, 'users/order_history.html', {"orders": orders})




