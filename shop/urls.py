from django.urls import path

from .views import (
    AddProductView,
    DeleteProductView,
    HomeView,
    CartView,
    CheckoutView,
    ProductView,
    UpdateProductView,
    VendorCustomersView,
    VendorDashboardView,
    VendorHomeView,
    VendorOrderView,
    VendorSettings,
    makepayment,
    AddToCart,
    quickview,
    reciept,
    validate_payment,
    DetailView,
    UpdateCart,
    remove_from_cart,
    Profile,
    CreateProfile,
    UpdateProfile,
)
from django.contrib.auth import views as auth_views

app_name = "store"
urlpatterns = [
    #  Index page
    path("", HomeView.as_view(), name="store"),
    # vendor home page
    # path("vendor/<slug>", VendorHomeView.as_view(), name="vendor-home"),
    # Shop Functionalities
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("cart/", CartView.as_view(), name="cart"),
    path("profile/", Profile.as_view(), name="profile"),
    path("profile/create/", CreateProfile.as_view(), name="profile-create"),
    path("profile/update/", UpdateProfile.as_view(), name="profile-update"),
    path("pay/", makepayment, name="makepayment"),
    path("verify/", validate_payment, name="verify-payment"),
    path("reciept/<slug:slug>/", reciept, name="reciept"),
    path("item-detail/<slug:slug>/", DetailView.as_view(), name="detail"),
    path("add-to-cart/", AddToCart, name="add-to-cart"),
    path("update_item/", UpdateCart, name="update-item"),
    path("remove_from_cart/<slug:slug>/", remove_from_cart, name="remove_from_cart"),
    path("get-item/", quickview),

    # Vendor Urls
    path("vendor/", VendorDashboardView.as_view(), name="vendor-home"),
    path("vendor/storefront/", VendorHomeView.as_view(),name="vendor-storefront"),#vendore storefront
    path("vendor/settings/", VendorSettings, name="vendor-settings"), #vendor settings
    path("vendor/orders/", VendorOrderView, name="vendor-orders"), #vendor orders
    path("vendor/products/", ProductView.as_view(), name="vendor-products"), #vendors Products
    path("vendor/add-product/", AddProductView.as_view(),name="add-product"),# vendor add products
    path("vendor/update-product/", UpdateProductView.as_view(),name="update-product"),# vendor update products
    path("vendor/delete-product/", DeleteProductView.as_view(),name="delete-product"),# vendor delete products
    path("vendor/customers/", VendorCustomersView.as_view(),name="vendor customers"),# vendor customers
]