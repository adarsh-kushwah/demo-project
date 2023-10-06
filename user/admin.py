from django.contrib import admin

from user.models import UserProfile
# Register your models here.
@admin.register(UserProfile)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["username","first_name"]