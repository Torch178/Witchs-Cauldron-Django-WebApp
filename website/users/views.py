from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RegistrationForm, ProfileForm, AddressForm
from django.contrib.auth.decorators import login_required
from .models import Profile

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
def profilepage(request):
    return render(request, 'users/profile.html')
@login_required()
def new_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            form.save()





