from calendar import c
from dataclasses import fields
from .models import Color, ProductItem, Size, UserProfile, Address
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
# Add to Cart form

class ProductAddToCartForm(forms.ModelForm):
    quantity = forms.IntegerField(
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Quantity',
            'id': 'qty',
            'type': 'number',
            'value': '1',
            'min': '1',
            'max': '100',
            'step': '1',
        }),
        initial=1
    )
    color = forms.ModelChoiceField(
        queryset=Color.objects.none(),  # Empty queryset initially
        widget=forms.Select(attrs={'class': 'color-radio'}),
        empty_label=None,
    )
    size = forms.ModelChoiceField(
        queryset=Size.objects.none(),  # Empty queryset initially
        widget=forms.Select(attrs={'class': 'size-radio'}),
        empty_label=None,
    )
    class Meta:
        model = ProductItem
        fields = ['quantity', 'color', 'size']

    def __init__(self, *args, **kwargs):
        # Extract the 'product_slug' parameter from the form's kwargs
        product_slug = kwargs.pop('product_slug', None)

        # Call the parent class's __init__ method
        super().__init__(*args, **kwargs)

        # Update the queryset for the color and size fields based on the selected product_slug
        if product_slug:
            product_items = ProductItem.objects.filter(product__slug=product_slug)
            self.fields['color'].queryset = Color.objects.filter(productitem__in=product_items)
            self.fields['size'].queryset = Size.objects.filter(productitem__in=product_items)
        
        # self.fields['color'].choices = [('', 'Choose color')] + list(self.fields['color'].choices)
        # self.fields['size'].choices = [('', 'Choose size')] + list(self.fields['size'].choices)

from django import forms
from .models import UserProfile, Gender_choices

class UserProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=Gender_choices)

    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'gender', 'email', 'phone']
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



class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['unit_number', 'street_number', 'address_line1', 'address_line2', 'city', 'state', 'postal_code', 'country']

class AddressUpdateForm(ModelForm):
    pass

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ("amount","email")

