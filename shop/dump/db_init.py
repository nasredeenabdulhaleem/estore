from shop.models import (
    Color,
    Size,
    Variation,
    OrderStatus,
)  # Replace with your actual model imports


def create_instances():
    # # Create Color instance
    color = Color.objects.get_or_create(name="Default", color="Default")

    # # Create Size instance
    size = Size.objects.get_or_create(title="Default", size="Default")

    # # Create Variation instances
    Variation.objects.get_or_create(name="Default")
    Variation.objects.get_or_create(name="Size")
    Variation.objects.get_or_create(name="Color")
    Variation.objects.get_or_create(name="Size and Color")

    # Create OrderStatus instances
    OrderStatus.objects.get_or_create(status="Awaiting Payment")
    OrderStatus.objects.get_or_create(status="Processing")
    OrderStatus.objects.get_or_create(status="Shipped")
    OrderStatus.objects.get_or_create(status="Delivered")
    OrderStatus.objects.get_or_create(status="Cancelled")
    OrderStatus.objects.get_or_create(status="Refunded")
    OrderStatus.objects.get_or_create(status="Completed")
    print("done")


# Call the function to start the instance creation
# create_instances()
