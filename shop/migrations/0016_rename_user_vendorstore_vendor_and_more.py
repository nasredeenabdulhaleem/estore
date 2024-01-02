# Generated by Django 4.2.7 on 2024-01-01 07:05

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0015_orderstatus_alter_order_status_delete_order_status"),
    ]

    operations = [
        migrations.RenameField(
            model_name="vendorstore",
            old_name="user",
            new_name="vendor",
        ),
        migrations.RenameField(
            model_name="vendorwallethistory",
            old_name="user",
            new_name="vendor",
        ),
        migrations.RemoveField(
            model_name="vendorstore",
            name="store_theme",
        ),
        migrations.AddField(
            model_name="vendorstore",
            name="store_logo",
            field=cloudinary.models.CloudinaryField(
                default="example.jpg", max_length=255, verbose_name="image"
            ),
            preserve_default=False,
        ),
    ]