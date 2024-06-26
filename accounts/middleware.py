# middleware.py

from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import VerificationCount
from shop.models import VendorStore


class VendorAccountVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exclude_urls = [
            reverse("account-verification"),
            reverse("admin:index"),
            reverse("resend-verification-email"),
            reverse("store:create-store"),
        ]
        if request.user.is_authenticated and request.user.role == "Vendor":
            verified = VerificationCount.objects.get(user=request.user).is_verified
            store_exists = VendorStore.objects.filter(
                vendor__user=request.user
            ).exists()
            if verified and request.path == reverse("account-verification"):
                return redirect(
                    "store:vendor-home", business_name=request.user.vendor.business_name
                )
            if (
                not request.path.startswith("/admin/")
                and not request.path.startswith("/accounts/verify-email/")
                and request.path not in exclude_urls
            ):
                # try:
                #     vendor = VendorStore.objects.get(
                #         vendor__business_name=request.user.vendor.business_name
                #     ).vendor
                # except VendorStore.DoesNotExist:
                #     raise Http404  # Explicitly signal a 404 error if vendor not found

                if not verified:
                    return redirect("account-verification")
                elif not store_exists:
                    return redirect("store:create-store")

        return self.get_response(request)
