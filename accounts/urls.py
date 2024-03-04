from django.urls import path
from .views import (
    ResendVerificationEmailView,
    UserSignup,
    Login,
    VerifyEmailView,
    account_verification,
    # deactivate_account,
    logout_view,
    update_password,
    vendor_login,
    vendor_signup,
)
from django.contrib.auth import views as auth_views

 
urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("signup/", UserSignup.as_view(), name="signup"),
    path("vendor-signup/", vendor_signup, name="vendor_signup"),
    path("<str:business_name>/login/", vendor_login, name="vendor_login"),
    path("logout", logout_view, name="logout"),
    path("account-verification/", account_verification, name="account-verification"),
    path(
        "resend-verification-email/",
        ResendVerificationEmailView.as_view(),
        name="resend-verification-email",
    ),
    path(
        "verify-email/<str:token>/",
        VerifyEmailView.as_view(),
        name="verify-email",
    ),
    path(
        "password-reset",
        auth_views.PasswordResetView.as_view(template_name="password-reset.html"),
        name="password_reset",
    ),
    path(
        "password-reset-done",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password-reset-done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password-reset-confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "password-reset-complete",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password-reset-complete.html"
        ),
        name="password_reset_complete",
    ),
    path("update_password/", update_password, name="update_password"),
    #  path('deactivate-account/', deactivate_account, name='deactivate_account'),
    #  path('reactivate/<uidb64>/<token>/', reactivate_account, name='reactivate_account'),
]
