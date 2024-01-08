# middleware.py

from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import VerificationCount
from shop.models import VendorStore


class VendorAccountVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        # List of views to exclude from the middleware
        exclude_urls = [
            reverse("account-verification"),
            reverse("store:vendor-mail"),
            reverse("admin:index")
            # Add more views to exclude here
        ]
        if request.user.is_authenticated and request.user.role == "Vendor":
            if (
                not request.path.startswith("/admin/")
                and request.path not in exclude_urls
            ):
                verified = VerificationCount.objects.filter(
                    user=request.user, is_verified=True
                ).exists()
                if not verified:
                    return redirect("account-verification")
                store_exists = VendorStore.objects.filter(
                    vendor__user=request.user
                ).exists()
                if not store_exists:
                    return redirect("create-store")

        return response
