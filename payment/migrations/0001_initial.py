# Generated by Django 4.2.6 on 2023-10-25 09:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        (
            "property",
            "0018_remove_payment_bill_remove_payment_user_delete_bill_and_more",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="Bill",
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
                ("amount", models.PositiveIntegerField()),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("paid", "Paid"),
                            ("partial_paid", "Partially paid"),
                            ("not_paid", "Not paid"),
                        ],
                        max_length=20,
                    ),
                ),
                ("document", models.FileField(null=True, upload_to="bills")),
                (
                    "month",
                    models.CharField(
                        choices=[
                            ("jan", "January"),
                            ("feb", "February"),
                            ("mar", "March"),
                            ("Apr", "April"),
                            ("may", "May"),
                            ("jun", "June"),
                            ("jul", "July"),
                            ("aug", "August"),
                            ("sep", "September"),
                            ("oct", "Octomber"),
                            ("nov", "November"),
                            ("dec", "December"),
                        ],
                        default="not_paid",
                        max_length=3,
                    ),
                ),
                ("year", models.PositiveIntegerField(null=True)),
                ("due_date", models.DateTimeField(null=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "booking",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="property.booking",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
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
                ("amount", models.PositiveIntegerField()),
                ("source", models.CharField(max_length=20)),
                ("status", models.CharField(max_length=10)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "bill",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="payment.bill"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
