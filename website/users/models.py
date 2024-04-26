from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Profile(models.Model):

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    profile_pic = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    registration_date = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.user.username

class Address(models.Model):
    streetAddress = models.CharField(max_length=200, blank=True, default='123 Easy Street')
    apartmentNum = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=200, blank=True, default='Party City')
    state = models.CharField(max_length=200, blank=True, default='Party State')
    country_region = models.CharField(max_length=200, blank=True, default='United States')
    zipcode = models.CharField(max_length=9, blank=True, default='000000000')
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, default=None)
    default_address = models.BooleanField(default=False)


    def __str__(self):
        if self.apartmentNum:
            return (self.streetAddress + ' '+ self.apartmentNum + ' ' + self.city +  ', ' + self.state + ' '+ self.zipcode)
        return (self.streetAddress + ' ' + self.city +  ', ' + self.state + ' '+ self.zipcode)

