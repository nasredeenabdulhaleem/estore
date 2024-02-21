from django import template
from django.contrib.auth.models import User

from chat.models import ChatUser

register = template.Library()


@register.simple_tag
def get_username_from_id(user_id):
    try:
        user = ChatUser.objects.get(chat_id=user_id).user
        return user.username
    except ChatUser.DoesNotExist:
        return "User"


@register.simple_tag
def get_vendor_name(receiver_id):
    try:
        user = ChatUser.objects.get(chat_id=receiver_id).user
        return user.vendor.business_name
    except ChatUser.DoesNotExist:
        return "User"
