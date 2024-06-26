# Generated by Django 4.2.7 on 2023-11-30 10:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0006_alter_cartitem_quantity_alter_orderitem_quantity_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="productitem",
            name="description",
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="userprofile",
            name="gender",
            field=models.CharField(
                choices=[("Male", "MALE"), ("Female", "FEMALE")], max_length=11
            ),
        ),
    ]
