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
            df = pd.read_excel(file_path)
            data = df.to_dict(orient="records")
            location_list = []
            counter = 1
            for row in data:
                state_city_pincode_dict = {key.lower(): str(value).capitalize()  for key, value in row.items()}
                if counter == 1:
                    keys_to_check = ["state", "city", "pincode"]
                    if not all(key in state_city_pincode_dict for key in keys_to_check):
                        self.stdout.write(
                            self.style.SUCCESS("Column name should be 'state' 'city' 'pincode'")
                        )
                        return
                    counter += 1
                
                state = row["state"]
                city = row["city"]
                pincode = row["pincode"]
                location_list.append(
                    Location(state=state, city=city, postal_code=pincode)
                )

            location = Location.objects.bulk_create(location_list)
            count_location = len(location)
            self.stdout.write(
                self.style.SUCCESS(
                    f"{'count_location'} location data populated successfully."
                )
            )

        except FileNotFoundError:
            self.stdout.write(self.style.ERROR("File not found."))
