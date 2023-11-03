from django.contrib import admin

from user.models import Location, UserProfile


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["state", "city", "postal_code"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = [
        "first_name",
        "last_name",
        "user_type",
        "date_of_birth",
        "gender",
        "marital_status",
        "profile_picture",
        "phone_number",
        "alternate_phone_number",
        "created_at",
    ]
