# Generates vendor admin identity

import secrets
from django.utils.text import slugify
import random
import uuid

def generate_vendor_id(firstname, lastname):
    vendor_id = f"{firstname[:3].upper()}{lastname[:3].upper()}{random.randint(100000, 999999)}"
    return slugify(vendor_id)

# Generates a unique order identifier
def generate_order_id():
    order_id = f"ORD-{uuid.uuid4}{secrets.token_urlsafe(10)}"
    return slugify(order_id)