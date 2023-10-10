from django.contrib import admin

from user.models import Location
from property.models import Property, PropertyImage


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["state", "city", "postal_code"]


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ["name"]


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ["image"]