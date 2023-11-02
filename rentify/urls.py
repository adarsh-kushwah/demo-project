from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from property.views import Home
from payment.views import my_webhook_view

urlpatterns = [
    path("", Home.as_view(), name="home"),
    path("user/", include("user.urls")),
    path("property/", include("property.urls")),
    path("rating/", include("rating.urls")),
    path("payment/", include("payment.urls")),
    path("admin/", admin.site.urls),
    path("webhook", my_webhook_view, name="webhook"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
