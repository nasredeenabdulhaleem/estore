# Generates vendor admin identity

import secrets
from django.utils.text import slugify
import random
import uuid


def generate_vendor_id():
    vendor_id = (
        f"VND{random.randint(100000, 999999)}"
    )
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
