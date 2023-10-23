from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path("user/", include("user.urls")),
    path("property/", include("property.urls")),
    path("rating/", include("rating.urls")),
    path("payment/", include("payment.urls")),
    path("admin/", admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
