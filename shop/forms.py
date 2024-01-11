from dataclasses import fields
from .models import Color, ProductItem, Size, UserProfile, Address, VendorStore
from django import forms
from django import forms
from .models import UserProfile, Gender_choices
from django.forms import ModelForm
from .models import Payment


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
            self.fields["color"].queryset = Color.objects.filter(
                productitem__in=product_items
            )

    def get_product_item(self):
        color = Color.objects.get(name="default")
        size = Size.objects.get(title="default")
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
