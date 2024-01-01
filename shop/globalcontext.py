from django.conf import settings

from shop.models import Cart, CartItem, OrderItem, VendorProfile


def my_global_context_processor(request):
    return {
        "site_name": settings.SITE_NAME,
        "site_url": settings.SITE_URL,
    }


def user_context_processor(request):
    user = request.user
    if user.is_anonymous:
        return {
            "cart": None,
            "total_items": 0,
            "total_price": 0,
        }

    # cart = OrderItem.objects.filter(user_id=user.id)
    # total = cart.get_total_order_price
    # # for item in cartitems:
    # #     total += item.quantity * item.product.product.price
    # total_items = cart.get_total_instances(request.user)

    if user.is_authenticated and Cart.objects.filter(user_id=user.id).exists():
        cart = Cart.objects.get(user=request.user)
        cartitems = CartItem.objects.filter(cart=cart).all()
        total = CartItem.get_total_order_price(cart=cart)
        # for item in cartitems:
        #     total += item.quantity * item.product.product.price
        total_items = CartItem.get_total_instances(request.user) or cartitems.count()

    else:
        cart = None
        cartitems = None
        total_items = 0
        total = 0

    return {
        "user": user,
        "cart": cart,
        "total_items": total_items,
        "total_price": total,
    }

def vendor_context_processor(request):
    user = request.user
    if user.is_anonymous:
        return {
            "business_name": "",
        }
    vendor = VendorProfile.objects.get(user=user)
    return vendor.business_name
    