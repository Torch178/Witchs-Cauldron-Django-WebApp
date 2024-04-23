from django import forms
from .models import Profile, Address
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['first_name', 'last_name','username', 'email', 'password1', 'password2']

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']

class PaymentForm(forms.Form):
    name = forms.CharField(label='Full Name',max_length=200, required=True)
    cardNumber = forms.DecimalField(label='Card Number',max_digits=16,decimal_places=0, required=True)
    expDate = forms.DateField(label='Expiration Date',input_formats=['%m/%y'], required=True )
    securityCode = forms.DecimalField(label='Security Code',max_digits=3,decimal_places=0, required=True)

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['__all__','profile']
        profile = forms.ModelChoiceField(
        )