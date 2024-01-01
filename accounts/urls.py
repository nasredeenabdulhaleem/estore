from django.urls import path
from .views import UserSignup, Login, VerifyEmailView, logout_view,vendor_login
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("signup/", UserSignup.as_view(), name="signup"),
    path("<str:business_name>/login/", vendor_login, name='vendor_login'),
    path("logout", logout_view, name="logout"),
    path(
        "accounts/verify-email/<str:token>/",
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
]
