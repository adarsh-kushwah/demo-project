# Generated by Django 4.2.6 on 2023-10-09 13:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("property", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="booking",
            name="end_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="booking",
            name="start_date",
            field=models.DateField(),
        ),
    ]
