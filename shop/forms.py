from calendar import c
from dataclasses import fields
from .models import UserProfile, Address
from django import forms
from django.forms import ModelForm
from .models import Payment


#class SignUpForm(forms.Form):
#    username = forms.CharField(
#        max_length=255, help_text="Username", widget=forms.TextInput)
#    email = forms.CharField(
#        max_length=255, help_text='jhondoe@gmail.com', widget=forms.EmailInput)
#    password = forms.CharField(max_length=255, widget=forms.PasswordInput)


#class LoginForm(forms.Form):
#    username = forms.CharField(max_length=255)
#    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
class UserUpdateForm(ModelForm):
    
    class Meta:
        model = UserProfile
        fields = [
            'firstname',
            'lastname',
            'email',
            # 'gender',
            'phone',
        ]
    

class AddressUpdateForm(ModelForm):
    class Meta:
        model = Address
        fields = ['address_line1', 'country',
                  'city', 'state']
        

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ("amount","email")

