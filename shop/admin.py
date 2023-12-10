from django.contrib import admin
from .models import (
    Cart,
    CartItem,
    Color,
    Country,
    Order_status,
    OrderHistory,
    Payment,
    PaymentMethod,
    PaymentType,
    ProductItem,
    ShippingMethod,
    Size,
    # Variation,
    VendorProfile,
    VendorStore,
    # Size,
    UserProfile,
    Product,
    Order,
    Mostpopular,
    Label,
    Address,
    Category,
    Picture,
    OrderItem,
    UserAddress,
    # Color,
    # ProductVaraiant,
)

# Register your models here.


class PictureInline(admin.StackedInline):
    model = Picture


class Popular(admin.ModelAdmin):
    model = Mostpopular


class ProductAdmin(admin.ModelAdmin):

    inlines = [PictureInline]
    prepopulated_fields = {"slug": ("title",)}
    list_display = [
        "title",
        "category_id"
    ]

    class Meta:
        model = Product


class OrderAdmin(admin.ModelAdmin):
    model: Order
    list_display = ["user", "ordered", "status", "received", "shipping_address"]
    list_display_links = ["user", "shipping_address"]
    list_filter = ["ordered", "status", "received"]
    search_fields = ["user__username"]


class CartAdmin(admin.ModelAdmin):
    model: Order
    list_display = [
        "user",
    ]
    list_display_links = ["user"]
    list_filter = ["user"]
    search_fields = ["user__username"]

    # def render_change_form(self, request, context, *args, **kwargs):
    #      context['adminform'].form.fields['items'].queryset = Order.objects.filter(user=Order.items.user)
    #      return super(OrderAdmin, self).render_change_form(request, context, *args, **kwargs)

# class SizeInline(admin.StackedInline):
#     model = Size

# class Productvariant(admin.ModelAdmin):
#     model: ProductVaraiant
#     # inlines = [SizeInline]
#     list_display = [
#         "product",
#         "color",
#     ]
#     list_filter = ["product"]
#     search_fields = ["product", "color"]


class AddressAdmin(admin.ModelAdmin):
    model: Address
    list_display = [
        "address_line1",
        "city",
        "state",
    ]
    list_filter = ["state"]
    search_fields = ["state"]


admin.site.register(UserProfile)
admin.site.register(Product, ProductAdmin)
admin.site.register(OrderItem, CartAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Label)
admin.site.register(Country)
admin.site.register(UserAddress)
admin.site.register(ShippingMethod)
admin.site.register(ProductItem)
admin.site.register(PaymentType)
admin.site.register(PaymentMethod)

admin.site.register(Mostpopular)
admin.site.register(OrderHistory)
# admin.site.register(ProductVaraiant, Productvariant)
admin.site.register(Address, AddressAdmin)
admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Size)
admin.site.register(Payment)
admin.site.register(Order_status)
admin.site.register(VendorProfile)
admin.site.register(VendorStore)
admin.site.register(Cart)
admin.site.register(CartItem)
# admin.site.register(Variation)