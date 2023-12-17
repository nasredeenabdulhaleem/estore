from django.urls import path
from .views import UserSignup, Login, logout_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("login/", Login.as_view(), name="login"),
    path("signup/", UserSignup.as_view(), name="signup"),
    path("logout", logout_view, name="logout"),
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
