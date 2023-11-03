from django.core.management.base import BaseCommand
import argparse
import pandas as pd
import os
from user.models import Location


class Command(BaseCommand):
    help = "Closes the specified poll for voting"
    """
    python manage.py populate_location location.xls
    """

    def add_arguments(self, parser):
        parser.add_argument("file_path", type=str, help="Excel file path")

    def handle(self, *args, **options):
        file_path = options["file_path"]

        try:
            df = pd.read_excel(file_path)  # Read the Excel file using pandas
            data = df.to_dict(orient="records")  # Convert DataFrame to dictionary
            location_list = []
            for row in data:
                state = row["state"]
                city = row["city"]
                pincode = str(row["pincode"])
                location_list.append(
                    Location(state=state, city=city, postal_code=pincode)
                )

            location = Location.objects.bulk_create(location_list)
            count_location = len(location)
            self.stdout.write(
                self.style.SUCCESS(
                    f"{count_location} location data populated successfully."
                )
            )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("File not found."))
