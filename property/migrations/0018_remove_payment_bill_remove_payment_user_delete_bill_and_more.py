# Generated by Django 4.2.6 on 2023-10-25 07:47

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("property", "0017_bill_due_date_bill_month_bill_year_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="payment",
            name="bill",
        ),
        migrations.RemoveField(
            model_name="payment",
            name="user",
        ),
        migrations.DeleteModel(
            name="Bill",
        ),
        migrations.DeleteModel(
            name="Payment",
        ),
    ]