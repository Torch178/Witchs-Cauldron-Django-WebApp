from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Profile


# Create your models here.

class Order(models.Model):
    subtotal = models.DecimalField(max_digits=20 ,decimal_places=2 , null=True)
    taxAmount = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    shipping = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    total = models.DecimalField(max_digits=20, decimal_places=2, null=True)
    orderDateTime = models.DateTimeField( null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='user_profiles')
    status = models.CharField(max_length=20 ,default='None')

    def __str__(self):
        return self.profile + "Order Number" + id()

    def calculate_order(self):
        order_items = OrderItem.objects.filter(order__id=self)
        for item in order_items:
            cost = (item.storeItem.price * item.quantity)
            self.subtotal += cost
        self.taxAmount += self.subtotal * 0.0725
        if self.subtotal > 100:
            self.shipping = 0
        else:
            self.shipping = self.subtotal / 100
        self.total = self.subtotal + self.taxAmount + self.shipping
        return self.total

class StoreItem(models.Model):
    image = models.ImageField(upload_to='store_item_images/', default='media/default.jpg')
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
    storeItem = models.ForeignKey(StoreItem, on_delete=models.CASCADE, related_name='store_item')
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    def __str__(self):
        return self.storeItem.name + ' - Order ID: ' + self.order.primary_key