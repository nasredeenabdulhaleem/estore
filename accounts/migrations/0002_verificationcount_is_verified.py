# Generated by Django 4.2.7 on 2023-11-21 19:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="verificationcount",
            name="is_verified",
            field=models.BooleanField(default=False),
        ),
    ]
