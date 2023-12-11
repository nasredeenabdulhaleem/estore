# Generated by Django 4.2.7 on 2023-12-10 20:42

import cloudinary.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0011_alter_product_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=cloudinary.models.CloudinaryField(max_length=255),
        ),
        migrations.AlterField(
            model_name='productitem',
            name='product_image',
            field=cloudinary.models.CloudinaryField(max_length=255),
        ),
    ]
