from store import settings
from django.urls import path, re_path

from .views import (
    # AddProductItemView,
    AddBankAccountView,
    AddProductItemView,
    AddProductView,
    ChangeWithdrawalPinView,
    CompleteOrderView,
    CreateAddress,
    DeleteProductItemView,
    DeleteProductView,
    HomeView,
    CartView,
    CheckoutView,
    OrderSummaryPDFView,
    ProductView,
    QRCodeView,
    SetWithdrawalPinView,
    UpdateAddress,
    UpdateProductItemView,
    UpdateProductView,
    VendorCustomersView,
    VendorDashboardView,
    VendorHomeView,
    VendorOrderView,
    VendorSettings,
    VendorWalletView,
    WalletHistoryView,
    WithdrawFundsView,
    create_store,
    # add_product_item,
    # add_product_item_color,
    # add_product_item_default,
    # add_product_item_size,
    # add_product_item_view,
    decreaseItem,
    increaseItem,
    makepayment,
    order_detail_view,
    # AddToCart,
    # quickview,
    # reciept,
    removeItem,
    search,
    send_email_to_users,
    send_email_to_vendors,
    update_vendor_profile,
    update_vendor_store,
    user_settings,
    # validate_payment,
    DetailView,
    # UpdateCart,
    # remove_from_cart,
    Profile,
    CreateProfile,
    UpdateProfile,
    vendor_product_detail,
    view_404,
)
from chat.views import UserChatListView
from django.contrib.auth import views as auth_views

app_name = "store"
handler404 = "shop.views.view_404"
handler500 = "shop.views.view_500"
handler403 = "shop.views.view_403"
handler302 = "shop.views.view_302"
handler302 = "shop.views.view_400"
# 48567322
urlpatterns = [
    #  Index page
    path("", HomeView.as_view(), name="home"),
    # path("chat/", UserChatListView.as_view(), name="chat"),
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
    path("item-detail/<slug:slug>/", DetailView.as_view(), name="detail"),
    path("vendor-mail/", send_email_to_vendors, name="vendor-mail"),
    path("user-mail/", send_email_to_users, name="user-mail"),
    path("qrcode/<store_name>/", QRCodeView.as_view(), name="qrcode"),
    # Vendor Urls
    path("create-store", create_store, name="create-store"),
    # path("update-store", update_vendor_store, name="update-store"),
    path("<str:business_name>/", VendorDashboardView.as_view(), name="vendor-home"),
    path(
        "store/<slug>/", VendorHomeView.as_view(), name="vendor-storefront"
    ),  # vendore storefront
    path(
        "<str:business_name>/update-profile/",
        update_vendor_profile,
        name="update_vendor_profile",
    ),
    path(
        "<str:business_name>/update-store/",
        update_vendor_store,
        name="update_vendor_store",
    ),
    path(
        "<str:business_name>/settings/", VendorSettings, name="vendor-settings"
    ),  # vendor settings
    path(
        "<str:business_name>/orders/", VendorOrderView, name="vendor-orders"
    ),  # vendor orders
    path(
        "<str:business_name>/order/<int:order_id>/",
        order_detail_view,
        name="vendor-order-detail",
    ),  # Vendor order detail view
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
        name="vendor-customers",
    ),  # vendor customers
    path(
        "<str:business_name>/wallet/",
        VendorWalletView.as_view(),
        name="vendor-wallet",
    ),  # vendor wallet
    path(
        "<str:business_name>/withdraw-funds/",
        WithdrawFundsView.as_view(),
        name="withdraw-funds",
    ),  # vendor withdraw funds
    path(
        "<str:business_name>/wallet-history/",
        WalletHistoryView.as_view(),
        name="wallet-history",
    ),  # vendor wallet history
    path(
        "<str:business_name>/add-bank-account/",
        AddBankAccountView.as_view(),
        name="add-bank-account",
    ),  # vendor add bank account
    path(
        "<str:business_name>/set-withdrawal-pin/",
        SetWithdrawalPinView.as_view(),
        name="set-withdrawal-pin",
    ),  # vendor set withdrawal pin
    path(
        "<str:business_name>/change-withdrawal-pin/",
        ChangeWithdrawalPinView.as_view(),
        name="change-withdrawal-pin",
    ),  # vendor change withdrawal pin
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r"^404/$", view_404),
    ]
