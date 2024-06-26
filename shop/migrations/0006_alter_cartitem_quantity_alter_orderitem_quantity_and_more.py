# Generated by Django 4.2.7 on 2023-11-25 04:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shop", "0005_cart_remove_order_items_remove_orderitem_order_id_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="cartitem",
            name="quantity",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="orderitem",
            name="quantity",
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="useraddress",
            name="address",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to="shop.address"
            ),
        ),
        migrations.AlterField(
            model_name="useraddress",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
