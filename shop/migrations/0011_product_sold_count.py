# Generated by Django 5.2.1 on 2025-06-20 22:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0010_order_shipping_postal_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="sold_count",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
