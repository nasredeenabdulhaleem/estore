from django import template
from django.forms import Textarea

register = template.Library()


@register.filter
def is_textarea(field):
    """
    Checks if the given field is a textarea widget.

    Args:
        field: The field to be checked.

    Returns:
        bool: True if the field is a textarea widget, False otherwise.
    """
    return isinstance(field.field.widget, Textarea)
