import secrets
import uuid
from django.db import models
from django.conf import settings
from django.urls import reverse
from shop.utils.enums import transaction_type_status

# for validators in user form
# to list countries in user form
from django_countries.fields import CountryField

# to list colors in the model fields
from colorfield.fields import ColorField

from shop.utils.utils import generate_order_id, generate_vendor_id

# this is used to add multiple images in the image field
# from autoslug import AutoSlugField
from .paystack import PayStack

# Create your models here.

Gender_choices = [("male", "MALE"), ("female", "FEMALE")]

Order_choices = [
    ("processing", "Processing"),
    ("Shipped", "Shipped"),
    ("delivered", "Delivered"),
    ("completed", "Order Completed"),
]
PROVIDERCHOICES = [
    ("processing", "Processing"),
    ("Shipped", "Shipped"),
    ("delivered", "Delivered"),
    ("completed", "Order Completed"),
]


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=255, null=False)
    lastname = models.CharField(max_length=255, null=False)
    gender = models.CharField(max_length=11, null=False)
    email = models.EmailField(max_length=255, null=False)
    phone = models.BigIntegerField(null=False)

    def __str__(self):
        return self.user.username


################# -----------Country--------#################


class Country(models.Model):
    country_name = models.CharField(max_length=25)

    def __str__(self):
        return self.country_name


################# -----------Address---------#################


class Address(models.Model):
    unit_number = models.IntegerField()
    street_number = models.IntegerField(verbose_name="Street Number")
    address_line1 = models.TextField(verbose_name="Address Line 1")
    address_line2 = models.TextField(verbose_name="Address Line 2")
    city = models.CharField(max_length=50, verbose_name="City")
    state = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=8, null=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)

    def __str__(self):
        return self.id


################# -----------User Address--------#################


class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username


################# -----------Shipping Method---------#################


class ShippingMethod(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField()

    def __str__(self):
        return self.name


################# -----------Category---------#################


class Category(models.Model):
    # category = models.ForeignKey("Category", on_delete=models.CASCADE)
    category = models.CharField(max_length=50)

    def __str__(self):
        return self.category_name


################# -----------Label--------#################


class Label(models.Model):
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


################# -----------Product---------#################


class Product(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    vendor = models.OneToOneField(
        "VendorProfile", on_delete=models.CASCADE, null=False, blank=False
    )
    category = models.OneToOneField("Category", on_delete=models.CASCADE, null=False)
    description = models.TextField(null=False, blank=False)
    image = models.ImageField(
        upload_to="product-image/", default="static/images/cart.png"
    )

    slug = models.SlugField(max_length=255, unique=True, default=uuid.uuid1)
    label = models.ForeignKey(Label, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.title

    # def add_to_cart_url(self):
    #     return reverse("store:add_to_cart", kwargs={"pk": self.pk})

    # @property
    # def soldout(self):
    #     if self.quantity_in_stock == 0:
    #         return True
    #     else:
    #         return False


################# -----------Product Item---------#################


class ProductItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    sku = models.CharField(max_length=15)
    quantity_in_stock = models.IntegerField()
    product_image = models.ImageField(
        upload_to="product-image/", default="static/images/cart.png"
    )
    price = models.FloatField()

    def __str__(self):
        return self.product.title


# ################# -----------PVariation--------#################


# class Variation(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     name = models.CharField(max_length=33)

#     def __str__(self):
#         return self.name


# ################# -----------Variation Option---------#################


# class VariationOption(models.Model):
#     variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
#     value = models.CharField(max_length=20)

#     def __str__(self):
#         return self.value


# ################# -----------Product Configuration---------#################


# class ProductConfiguration(models.Model):
#     product_item = models.ForeignKey(ProductItem, on_delete=models.CASCADE)
#     variation_option = models.ForeignKey(VariationOption, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.value


# ################# -----------Promotion---------#################


# class Promotion(models.Model):
#     name = models.CharField(max_length=50)
#     description = models.TextField()
#     discount_rate = models.IntegerField()
#     start_date = models.DateTimeField()
#     end_date = models.DateTimeField()


# ################# -----------Promotion Category---------#################


# class PromotionCategory(models.Model):
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.value


################# -----------Product Item---------#################
################# -----------Product Item---------#################
################# -----------Product Item---------#################


class Picture(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to="product-image/")

    def __str__(self):
        return self.picture.url


class Color(models.Model):
    name = models.CharField(max_length=255, null=True)
    color = ColorField(default="#FF0000", null=True)

    def __str__(self):
        return self.name


class Size(models.Model):
    title = models.CharField(max_length=255, null=True)
    size = models.CharField(max_length=255)

    # class Meta:

    #     fields = [
    #         "title",
    #         "size"
    #     ]

    def __str__(self):
        return self.title


class ProductVaraiant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, unique=True, default=uuid.uuid1)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=False, blank=False)
    size = models.ManyToManyField("Size")
    sku = models.CharField(max_length=20)
    amount_in_stock = models.IntegerField()
    # available = models.BooleanField(default=False)

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=[
#                     "product",
#                     "color",
#                 ],
#                 name="unique_prod_color_combo",
#             )
#         ]

#     def __str__(self):
#         return f"{self.product.title} "

#     # def size(self):
#     #     return ', '.join([a.size for a in self.size.all()])

#     @property
#     def instock(self):
#         return sum(self.amount_in_stock)


################# -----------Most Popular Product---------#################
class Mostpopular(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["product"], name="unique_prod")]

    def __str__(self):
        return self.product.title


################# ----------- End Product---------#################


class OrderItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(ProductItem, on_delete=models.CASCADE, blank=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.product.title}"

    @property
    def get_total_item_price(self):
        return self.quantity * self.product.price

    @property
    def get_final_price(self):
        return self.get_total_item_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered_date = models.DateTimeField(auto_now_add=True)
    items = models.ManyToManyField("OrderItem")
    ref = models.CharField(max_length=200)
    order_notes = models.TextField(blank=True, null=True)
    ordered = models.BooleanField(default=False)
    shipping_address = models.ForeignKey(
        "Address", on_delete=models.SET_NULL, blank=True, null=True
    )
    status = models.ForeignKey(
        "Order_status", on_delete=models.SET_NULL, blank=True, null=True
    )
    received = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        while not self.ref:
            ref = generate_order_id()
            object_with_similar_ref = Order.objects.filter(ref=ref)
            if not object_with_similar_ref:
                self.ref = ref
        super().save(*args, **kwargs)


class OrderHistory(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)


class Order_status(models.Model):
    status = models.CharField(
        choices=Order_choices, max_length=20, default="processing", null=False
    )

    def __str__(self):
        return self.status


# Payement models


class PaymentType(models.Model):
    value = models.CharField(max_length=33)

    def __str__(self):
        return self.value


class PaymentMethod(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE)
    provider = models.CharField(max_length=60, choices=PROVIDERCHOICES)
    account_number = models.CharField(max_length=12)
    expiry_date = models.DateField()
    is_default = models.BooleanField()

    def __str__(self):
        return self.user.username


class Payment(models.Model):
    amount = models.PositiveIntegerField()
    ref = models.CharField(max_length=200)
    email = models.EmailField()
    verified = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("-date_created",)

    def __str__(self) -> str:
        return f"Payment:  {self.amount}"

    def amount_value(self) -> int:
        return self.amount * 100

    def verify_payment(self):
        paystack = PayStack()
        status, result = paystack.verify_payment(self.ref, self.amount)
        if status:
            if result["amount"] / 100 == self.amount:
                self.verified = True
            self.save()
        if self.verified:
            return True
        return False


class RequestedRefund(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)


###################################################################################################
######################################Vendor Models Section########################################
###################################################################################################

# Vendor Profile Information


class VendorProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    vendor_id = models.CharField(max_length=255, null=False)
    firstname = models.CharField(max_length=255, null=False)
    lastname = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=11,null=False)
    email = models.EmailField(null=False)
    address = models.ForeignKey(Address, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.vendor_id:
            self.vendor_id = generate_vendor_id(self.firstname, self.lastname)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.vendor_id


# Vendor Bank Information


class VendorBank(models.Model):
    user = models.OneToOneField(VendorProfile, on_delete=models.CASCADE)
    bank_name = models.CharField(max_length=255, null=False)
    account_number = models.CharField(max_length=255, null=False)
    account_name = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.user.vendor_id


# Vendor Store Information


class VendorStore(models.Model):
    user = models.OneToOneField(VendorProfile, on_delete=models.CASCADE)
    store_name = models.CharField(max_length=255, null=False)
    store_address = models.ForeignKey(Address, on_delete=models.CASCADE)
    store_theme = models.CharField(max_length=255, null=False)

    def __str__(self):
        return self.user.vendor_id


# Vendor Wallet Account


class VendorWallet(models.Model):
    user = models.OneToOneField(VendorProfile, on_delete=models.CASCADE)
    wallet_balance = models.IntegerField(null=False)

    def __str__(self):
        return self.user.vendor_id


# Vendor Wallet History


class VendorWalletHistory(models.Model):
    user = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    reference = models.CharField(max_length=255, null=False, default=uuid.uuid4)
    wallet_balance = models.IntegerField(null=False)
    transaction_type = models.CharField(
        max_length=255, null=False, choices=transaction_type_status
    )
    description = models.TextField(max_length=610, null=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.vendor_id


# Vendor Order


class VendorOrder(models.Model):
    user = models.ForeignKey(VendorProfile, on_delete=models.CASCADE)
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.vendor_id
