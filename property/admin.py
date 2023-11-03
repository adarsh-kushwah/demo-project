from django.contrib import admin

from user.models import Location
from property.models import Property, PropertyImage


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    list_filter = ["name", "property_type"]
    ordering = ["name", "is_available"]


@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ["image"]
