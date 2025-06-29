# Generated by Django 5.2.1 on 2025-06-11 21:08

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0007_alter_order_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="code",
            field=models.CharField(
                default=uuid.uuid4, editable=False, max_length=36, unique=True
            ),
        ),
    ]
