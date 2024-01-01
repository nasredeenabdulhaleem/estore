from store import settings
from django.urls import path, re_path

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
    view_404,
)
from django.contrib.auth import views as auth_views

app_name = "store"
handler404 = "shop.views.view_404"
handler500 = "shop.views.view_500"
handler403 = "shop.views.view_403"
urlpatterns = [
    #  Index page
    path("", HomeView.as_view(), name="store"),
    path("search/", search, name="search"),
    # vendor home page
    # path("vendor/<slug>", VendorHomeView.as_view(), name="vendor-home"),
    # Shop Functionalities
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("cart/", CartView.as_view(), name="cart"),
    path(
        "complete_order/<slug:order_ref>/",
        CompleteOrderView.as_view(),
        name="complete_order",
    ),  # Complete Order
    path(
        "Order-Summary/<slug:order_ref>/",
        OrderSummaryPDFView.as_view(),
        name="order_summary_pdf",
    ),  # Order Summary PDF
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
    path("<str:business_name>/", VendorDashboardView.as_view(), name="vendor-home"),
    path(
        "store/<slug>/", VendorHomeView.as_view(), name="vendor-storefront"
    ),  # vendore storefront
    path(
        "<str:business_name>/settings/", VendorSettings, name="vendor-settings"
    ),  # vendor settings
    path(
        "<str:business_name>/orders/", VendorOrderView, name="vendor-orders"
    ),  # vendor orders
    path(
        "<str:business_name>/products/", ProductView.as_view(), name="vendor-products"
    ),  # vendors Products
    path(
        "<str:business_name>/product/<slug:slug>/",
        vendor_product_detail,
        name="vendor_product_detail",
    ),
    path(
        "<str:business_name>/add-product/", AddProductView.as_view(), name="add-product"
    ),  # vendor add products
    path(
        "<str:business_name>/update-product/<slug:slug>/",
        UpdateProductView.as_view(),
        name="update-product",
    ),  # vendor update products
    path(
        "<str:business_name>/delete-product/<slug:slug>/",
        DeleteProductView.as_view(),
        name="delete-product",
    ),  # vendor delete products
    path(
        "<str:business_name>/productitem/<slug:slug>/create",
        AddProductItemView.as_view(),
        name="add-product-item",
    ),  # vendor add product item
    path(
        "<str:business_name>/productitem/<int:pk>/update",
        UpdateProductItemView.as_view(),
        name="update-product-item",
    ),  # vendor update product item
    path(
        "<str:business_name>/productitem/<int:pk>/delete/",
        DeleteProductItemView.as_view(),
        name="delete-product-item",
    ),
    path(
        "<str:business_name>/customers/",
        VendorCustomersView.as_view(),
        name="vendor customers",
    ),  # vendor customers
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r"^404/$", view_404),
    ]
