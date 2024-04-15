from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics', default='default.jpg')
    registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class Address(models.Model):
    streetAddress = models.CharField(max_length=200, blank=True)
    apartmentNum = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    country_region = models.CharField(max_length=200, blank=True)
