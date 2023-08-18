# Generated by Django 4.2.4 on 2023-08-16 10:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("shop", "0005_rename_items_order_products"),
    ]

    operations = [
        migrations.CreateModel(
            name="Checkout",
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
                ("street_address", models.CharField(max_length=100)),
                ("apartment_address", models.CharField(blank=True, max_length=100)),
                ("country", django_countries.fields.CountryField(max_length=2)),
                ("zip", models.CharField(max_length=100)),
                ("city", models.CharField(max_length=50)),
                (
                    "order",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="checkout",
                        to="shop.order",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
