from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    profile_pic = models.ImageField(upload_to='profile_pics/', default='media/default.jpg')
    registration_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username

class Address(models.Model):
    streetAddress = models.CharField(max_length=200, blank=True)
    apartmentNum = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=200, blank=True)
    state = models.CharField(max_length=200, blank=True)
    country_region = models.CharField(max_length=200, blank=True)
    zipcode = models.DecimalField(max_digits=9, decimal_places=0, blank=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    primary_address = models.BooleanField(default=False)

