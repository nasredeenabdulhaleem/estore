# Generated by Django 4.2.7 on 2024-02-21 13:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0023_bankaccount_vendorwallethistory_amount_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vendorstore",
            name="vendor",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="store",
                to="shop.vendorprofile",
            ),
        ),
    ]
