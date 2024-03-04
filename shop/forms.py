from dataclasses import fields
from .models import (
    BankAccount,
    Color,
    ProductItem,
    Size,
    UserProfile,
    Address,
    VendorProfile,
    VendorStore,
    VendorWithdrawal,
    WithdrawalPin,
)
from django import forms
from django import forms
from .models import UserProfile, Gender_choices
from django.forms import ModelForm
from .models import Payment
import bcrypt
from django.core.exceptions import ValidationError


# class SignUpForm(forms.Form):
#    username = forms.CharField(
#        max_length=255, help_text="Username", widget=forms.TextInput)
#    email = forms.CharField(
#        max_length=255, help_text='jhondoe@gmail.com', widget=forms.EmailInput)
#    password = forms.CharField(max_length=255, widget=forms.PasswordInput)


# class LoginForm(forms.Form):
#    username = forms.CharField(max_length=255)
#    password = forms.CharField(max_length=255, widget=forms.PasswordInput)
# Add to Cart form


class ProductAddToCartForm(forms.ModelForm):
    quantity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Quantity",
                "id": "qty",
                "type": "number",
                "value": "1",
                "min": "1",
                "max": "100",
                "step": "1",
            }
        ),
        initial=1,
    )
    color = forms.ModelChoiceField(
        queryset=Color.objects.none(),  # Empty queryset initially
        widget=forms.Select(attrs={"class": "color-radio"}),
        empty_label=None,
    )
    size = forms.ModelChoiceField(
        queryset=Size.objects.none(),  # Empty queryset initially
        widget=forms.Select(attrs={"class": "size-radio"}),
        empty_label=None,
    )

    class Meta:
        model = ProductItem
        fields = ["quantity", "color", "size"]

    def __init__(self, *args, **kwargs):
        # Extract the 'product_slug' parameter from the form's kwargs
        product_slug = kwargs.pop("product_slug", None)

        # Call the parent class's __init__ method
        super().__init__(*args, **kwargs)

        # Update the queryset for the color and size fields based on the selected product_slug
        if product_slug:
            product_items = ProductItem.objects.filter(product__slug=product_slug)
            self.fields["color"].queryset = Color.objects.filter(
                productitem__in=product_items
            )
            self.fields["size"].queryset = Size.objects.filter(
                productitem__in=product_items
            )

    def get_product_item(self):
        color = self.cleaned_data.get("color")
        size = self.cleaned_data.get("size")
        if color and size:
            return ProductItem.objects.filter(color=color, size=size).first()
        return None


class ProductAddToCartFormV3(forms.ModelForm):
    quantity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Quantity",
                "id": "qty",
                "type": "number",
                "value": "1",
                "min": "1",
                "max": "100",
                "step": "1",
            }
        ),
        initial=1,
    )

    size = forms.ModelChoiceField(
        queryset=Size.objects.none(),  # Empty queryset initially
        widget=forms.Select(attrs={"class": "size-radio"}),
        empty_label=None,
    )

    class Meta:
        model = ProductItem
        fields = ["quantity", "color", "size"]

    def __init__(self, *args, **kwargs):
        # Extract the 'product_slug' parameter from the form's kwargs
        product_slug = kwargs.pop("product_slug", None)

        # Call the parent class's __init__ method
        super().__init__(*args, **kwargs)

        # Update the queryset for the size fields based on the selected product_slug
        if product_slug:
            product_items = ProductItem.objects.filter(product__slug=product_slug)
            self.fields["size"].queryset = Size.objects.filter(
                productitem__in=product_items
            )

    def get_product_item(self):
        size = self.cleaned_data.get("size")
        if size:
            return ProductItem.objects.filter(size=size).first()
        return None


class ProductAddToCartFormV2(forms.ModelForm):
    quantity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Quantity",
                "id": "qty",
                "type": "number",
                "value": "1",
                "min": "1",
                "max": "100",
                "step": "1",
            }
        ),
        initial=1,
    )

    class Meta:
        model = ProductItem
        fields = ["quantity", "color"]

    def __init__(self, *args, **kwargs):
        # Extract the 'product_slug' parameter from the form's kwargs
        product_slug = kwargs.pop("product_slug", None)

        # Call the parent class's __init__ method
        super().__init__(*args, **kwargs)

        # Update the queryset for the color fields based on the selected product_slug
        if product_slug:
            product_items = ProductItem.objects.filter(product__slug=product_slug)
            self.fields["color"].queryset = Color.objects.filter(
                productitem__in=product_items
            )

    def get_product_item(self):
        color = self.cleaned_data.get("color")
        if color:
            return ProductItem.objects.filter(color=color).first()
        return None


class ProductAddToCartFormV1(forms.ModelForm):
    quantity = forms.IntegerField(
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "Quantity",
                "id": "qty",
                "type": "number",
                "value": "1",
                "min": "1",
                "max": "100",
                "step": "1",
            }
        ),
        initial=1,
    )

    class Meta:
        model = ProductItem
        fields = ["quantity"]

    def __init__(self, *args, **kwargs):
        # Extract the 'product_slug' parameter from the form's kwargs
        product_slug = kwargs.pop("product_slug", None)

        # Call the parent class's __init__ method
        super().__init__(*args, **kwargs)

        # Update the queryset for the color fields based on the selected product_slug
        if product_slug:
            product_items = ProductItem.objects.filter(product__slug=product_slug)
            # self.fields["color"].queryset = Color.objects.filter(
            #     productitem__in=product_items
            # )

    def get_product_item(self):
        color = Color.objects.get(name="Default")
        size = Size.objects.get(title="Default")
        if color and size:
            return ProductItem.objects.filter(color=color, size=size).first()
        return None


class UserProfileForm(forms.ModelForm):
    gender = forms.ChoiceField(choices=Gender_choices)

    class Meta:
        model = UserProfile
        fields = ["firstname", "lastname", "gender", "email", "phone"]


class UserUpdateForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "firstname",
            "lastname",
            "email",
            # 'gender',
            "phone",
        ]


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            "first_name",
            "last_name",
            "shipping_address",
            "billing_address",
            "city",
            "state",
            "postal_code",
            "country",
        ]


class AddressUpdateForm(ModelForm):
    pass


class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ("amount", "email")


class CheckoutForm(forms.Form):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    phone_number = forms.CharField(max_length=15)
    shipping_address = forms.CharField(widget=forms.Textarea)
    billing_address = forms.CharField(widget=forms.Textarea)
    city = forms.CharField(max_length=30)  # Add this line
    state = forms.CharField(max_length=30)  # Add this line
    postal_code = forms.CharField(max_length=10)  # Add this line
    country = forms.CharField(max_length=30)  # Add this line
    save_info = forms.BooleanField(required=False)


class VendorStoreForm(forms.ModelForm):
    class Meta:
        model = VendorStore
        fields = [
            "store_name",
            "store_address",
            "store_logo",
            "store_description",
            "store_category",
            "store_sub_category",
            "store_country",
            "store_state",
            "store_city",
        ]


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ["bank_name", "account_name", "account_number"]


class WithdrawalPinForm(forms.ModelForm):
    confirm_pin = forms.CharField(max_length=255)

    class Meta:
        model = WithdrawalPin
        fields = ["pin", "confirm_pin"]

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get("pin")
        confirm_pin = cleaned_data.get("confirm_pin")

        if pin != confirm_pin:
            raise ValidationError("Pin not the same")

        return cleaned_data


class VendorWithdrawalForm(forms.ModelForm):
    pin = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = VendorWithdrawal
        fields = ["bank_account", "amount", "pin"]

    def __init__(self, *args, **kwargs):
        self.vendor = kwargs.pop("vendor", None)
        super(VendorWithdrawalForm, self).__init__(*args, **kwargs)
        if self.vendor:
            self.fields["bank_account"].queryset = BankAccount.objects.filter(
                vendor=self.vendor.user.vendor
            )

    def clean(self):
        cleaned_data = super().clean()
        pin = cleaned_data.get("pin")
        if self.vendor and pin:
            hashed_pin = self.vendor.withdrawalpin.pin
            if not bcrypt.checkpw(pin.encode(), hashed_pin.encode()):
                raise ValidationError("Pin invalid")
        return cleaned_data


class ChangeWithdrawalPinForm(forms.Form):
    previous_pin = forms.CharField(widget=forms.PasswordInput)
    new_pin = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        self.vendor = kwargs.pop("vendor", None)
        super(ChangeWithdrawalPinForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        previous_pin = cleaned_data.get("previous_pin")
        new_pin = cleaned_data.get("new_pin")
        if self.vendor and previous_pin and new_pin:
            hashed_pin = self.vendor.withdrawalpin.pin
            if not bcrypt.checkpw(previous_pin.encode(), hashed_pin.encode()):
                raise ValidationError("Previous pin incorrect")
            else:
                hashed_new_pin = bcrypt.hashpw(new_pin.encode(), bcrypt.gensalt())
                self.vendor.withdrawalpin.pin = hashed_new_pin.decode()
                self.vendor.withdrawalpin.save()
        return cleaned_data


class VendorProfileForm(forms.ModelForm):
    class Meta:
        model = VendorProfile
        fields = ["firstname", "lastname", "email", "phone", "email", "address"]
