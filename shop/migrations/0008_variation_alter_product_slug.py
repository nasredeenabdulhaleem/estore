# Generated by Django 4.2.7 on 2023-12-10 06:41

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0007_productitem_description_alter_userprofile_gender"),
    ]

    operations = [
        migrations.CreateModel(
            name="Variation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(default="Default", max_length=33)),
            ],
        ),
        migrations.AlterField(
            model_name="product",
            name="slug",
            field=models.SlugField(max_length=255, unique=True),
        ),
    ]
