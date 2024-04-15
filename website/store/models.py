from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile


# Create your models here.

class Order(models.Model):
    subtotal = models.DecimalField(max_digits=20 ,decimal_places=2)
    taxAmount = models.DecimalField(max_digits=20, decimal_places=2)
    shipping = models.DecimalField(max_digits=20, decimal_places=2)
    total = models.DecimalField(max_digits=20, decimal_places=2)
    orderDateTime = models.DateTimeField()
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)

class StoreItem(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    manufacturer = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    quantityAvailable = models.IntegerField()
    totalSold = models.IntegerField()

    def __str__(self):
        return self.name

class OrderItem(models.Model):
    quantity = models.IntegerField()
    storeItem = models.ForeignKey(StoreItem, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.storeItem.name + ' - Order ID: ' + self.order.primary_key