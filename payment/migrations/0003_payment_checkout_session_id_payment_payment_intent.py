# Generated by Django 4.2.6 on 2023-10-30 12:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0002_alter_payment_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="payment",
            name="checkout_session_id",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name="payment",
            name="payment_intent",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
