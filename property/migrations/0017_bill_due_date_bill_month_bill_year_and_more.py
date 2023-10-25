# Generated by Django 4.2.6 on 2023-10-25 07:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("property", "0016_bill_document"),
    ]

    operations = [
        migrations.AddField(
            model_name="bill",
            name="due_date",
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name="bill",
            name="month",
            field=models.CharField(
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
                max_length=3,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="bill",
            name="year",
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name="bill",
            name="created_at",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]