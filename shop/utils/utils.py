# Generates vendor admin identity

import functools
import secrets
from django.utils.text import slugify
import random
import uuid
from django.contrib.auth.decorators import user_passes_test
from django.urls import reverse
from django.contrib.auth.views import REDIRECT_FIELD_NAME


def generate_vendor_id():
    vendor_id = f"VND{random.randint(100000, 999999)}"
    return slugify(vendor_id)


# Generates a unique order identifier
def generate_order_id():
    order_id = f"ORD-{uuid.uuid4}{secrets.token_urlsafe(10)}"
    return slugify(order_id)


# Sluggify Product Title
# def slugify_product_title(product_title):

#     return slugify(product_title)


# Generates a unique product slug for a product from it title
def slugify_product_title(product_title):
    product_slug = f"{slugify(product_title)}-{uuid.uuid4()}{secrets.token_urlsafe(10)}"
    return slugify(product_slug)[:32]


# Generates a unique sku for a product item from it product title


def generate_sku(title, category, color, size):
    # Get product attributes
    product_type = category
    color = color
    size = size

    # Create SKU
    sku = f"{title}-{product_type}-{color}-{size}-{uuid.uuid4()}"

    # Ensure SKU is not too long
    sku = sku[:15]

    return sku


def user_passes_test_with_args(
    test_func, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME
):
    def decorator(view_func):
        @functools.wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            # Call test_func with user and business_name
            if test_func(request.user, kwargs["business_name"]):
                # If test_func returns True, call the view normally.
                return view_func(request, *args, **kwargs)
            else:
                # If test_func returns False, redirect to login.
                from django.contrib.auth.views import redirect_to_login

                path = request.build_absolute_uri()
                # Include business_name in the login URL
                resolved_login_url = reverse(
                    login_url, kwargs={"business_name": kwargs["business_name"]}
                )
                return redirect_to_login(path, resolved_login_url, redirect_field_name)

        return _wrapped_view

    return decorator
