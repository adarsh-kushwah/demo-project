from django.contrib import admin

from user.models import Location
# Register your models here.
@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["state", "city", "postal_code"]