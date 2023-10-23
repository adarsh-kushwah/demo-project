from django.urls import path, include
from django.contrib.auth import views as auth_views
from payment.views import GenerateBillView


urlpatterns = [
    path("generate-bill/", GenerateBillView.as_view(), name="property_rating"),
]
