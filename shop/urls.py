from django.urls import path

from .views import (
    # AddProductItemView,
    AddProductItemView,
    AddProductView,
    CompleteOrderView,
    CreateAddress,
    DeleteProductItemView,
    DeleteProductView,
    HomeView,
    CartView,
    CheckoutView,
    OrderSummaryPDFView,
    ProductView,
    UpdateAddress,
    UpdateProductItemView,
    UpdateProductView,
    VendorCustomersView,
    VendorDashboardView,
    VendorHomeView,
    VendorOrderView,
    VendorSettings,
    # add_product_item,
    # add_product_item_color,
    # add_product_item_default,
    # add_product_item_size,
    # add_product_item_view,
    decreaseItem,
    increaseItem,
    makepayment,
    AddToCart,
    quickview,
    reciept,
    removeItem,
    search,
    user_settings,
    validate_payment,
    DetailView,
    UpdateCart,
    remove_from_cart,
    Profile,
    CreateProfile,
    UpdateProfile,
    vendor_product_detail,
)
from django.contrib.auth import views as auth_views

app_name = "store"
urlpatterns = [
    #  Index page
    path("", HomeView.as_view(), name="store"),
    path("search/", search, name="search"),
    # vendor home page
    # path("vendor/<slug>", VendorHomeView.as_view(), name="vendor-home"),
    # Shop Functionalities
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("cart/", CartView.as_view(), name="cart"),
    path('complete_order/<slug:order_ref>/', CompleteOrderView.as_view(), name='complete_order'), # Complete Order
    path("Order-Summary/<slug:order_ref>/", OrderSummaryPDFView.as_view(), name="order_summary_pdf"), # Order Summary PDF
    # User Urls
    path("settings/", user_settings, name="user_settings"),
    path("profile/", Profile, name="profile"),
    path("profile/create/", CreateProfile.as_view(), name="create-profile"),
    path("profile/update/", UpdateProfile.as_view(), name="update-profile"),
    path("address/create/", CreateAddress.as_view(), name="create-address"),
    path("address/update/", UpdateAddress.as_view(), name="update-address"),
    # Cart Functionalities
    path("increaseitem/<id>/", increaseItem, name="additem"),
    path("decreaseitem/<id>/", decreaseItem, name="reduceitem"),
    path("removeitem/<id>/", removeItem, name="removeitem"),
    path("pay/", makepayment, name="makepayment"),
    path("verify/", validate_payment, name="verify-payment"),
    path("reciept/<slug:slug>/", reciept, name="reciept"),
    path("item-detail/<slug:slug>/", DetailView.as_view(), name="detail"),
    path("add-to-cart/", AddToCart, name="add-to-cart"),
    path("update_item/", UpdateCart, name="update-item"),
    path("remove_from_cart/<slug:slug>/", remove_from_cart, name="remove_from_cart"),  # type: ignore
    path("get-item/", quickview),
    # Vendor Urls
    path("vendor/", VendorDashboardView.as_view(), name="vendor-home"),
    path(
        "vendor/storefront/", VendorHomeView.as_view(), name="vendor-storefront"
    ),  # vendore storefront
    path("vendor/settings/", VendorSettings, name="vendor-settings"),  # vendor settings
    path("vendor/orders/", VendorOrderView, name="vendor-orders"),  # vendor orders
    path(
        "vendor/products/", ProductView.as_view(), name="vendor-products"
    ),  # vendors Products
    path(
        "vendor/product/<slug:slug>/",
        vendor_product_detail,
        name="vendor_product_detail",
    ),
    path(
        "vendor/add-product/", AddProductView.as_view(), name="add-product"
    ),  # vendor add products
    path(
        "vendor/update-product/<slug:slug>/",
        UpdateProductView.as_view(),
        name="update-product",
    ),  # vendor update products
    path(
        "vendor/delete-product/<slug:slug>/",
        DeleteProductView.as_view(),
        name="delete-product",
    ),  # vendor delete products
    path(
        "vendor/productitem/<slug:slug>/create",
        AddProductItemView.as_view(),
        name="add-product-item",
    ),  # vendor add product item
    path(
        "vendor/productitem/<int:pk>/update",
        UpdateProductItemView.as_view(),
        name="update-product-item",
    ),  # vendor update product item
    path(
        "vendor/productitem/<int:pk>/delete/",
        DeleteProductItemView.as_view(),
        name="delete-product-item",
    ),
    path(
        "vendor/customers/", VendorCustomersView.as_view(), name="vendor customers"
    ),  # vendor customers
]
