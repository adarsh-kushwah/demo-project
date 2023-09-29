from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("user/", include("user.urls")),
    path("property/", include("property.urls")),
    path("admin/", admin.site.urls),
]
