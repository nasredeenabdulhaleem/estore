# middleware.py

from django.shortcuts import redirect
from django.urls import reverse
from accounts.models import VerificationCount
from shop.models import VendorStore


class VendorAccountVerificationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        exclude_urls = [reverse("account-verification"), reverse("admin:index")]
        if request.user.is_authenticated and request.user.role == "Vendor":
            if (
                not request.path.startswith("/admin/")
                and request.path not in exclude_urls
            ):
                verified = VerificationCount.objects.get(user=request.user).is_verified
                store_exists = VendorStore.objects.filter(
                    vendor__user=request.user
                ).exists()
                print(verified, store_exists)

                if not verified:
                    print("not verified")
                    return redirect("account-verification")
                elif not store_exists:
                    return redirect("create-store")
                elif verified and request.path == reverse("account-verification"):
                    return redirect(
                        "store:vendor-home",
                        kwargs={"business_name": request.user.vendor.business_name},
                    )

        return self.get_response(request)
