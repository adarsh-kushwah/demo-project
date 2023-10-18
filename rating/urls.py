from django.urls import path, include
from django.contrib.auth import views as auth_views
from rating.views import PropertyRatingView, RenterRatingView


urlpatterns = [
    path("property/<int:booking_id>/", PropertyRatingView.as_view(), name="property_rating"),
    path("renter/<int:booking_id>/", RenterRatingView.as_view(), name="renter_rating"),
]