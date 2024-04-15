from django.shortcuts import render, redirect
from django.template import loader
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from store.models import StoreItem


# Create your views here.

def home(request):
    template = loader.get_template('store/home.html')
    return render(request, 'store/home.html')

def browse(request):
    template = loader.get_template('store/listings.html')
    item_list = StoreItem.objects.all()
    return render(request, 'store/listings.html', {'item_list': item_list})

def add_to_cart(request, id):
    item = StoreItem.objects.get(pk=id)
    return render(request, 'store/home.html')