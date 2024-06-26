# Generated by Django 5.0.6 on 2024-05-30 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("coupons", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coupon",
            name="amount",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
        migrations.AlterField(
            model_name="coupon",
            name="customer_names",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="coupon",
            name="customer_phone",
            field=models.CharField(blank=True, max_length=11, null=True),
        ),
    ]
