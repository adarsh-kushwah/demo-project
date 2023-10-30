from django.urls import path, include
from django.contrib.auth import views as auth_views
from rating.views import (
    PropertyRatingView,
    RenterRatingView,
    PropertyReviewView,
    RenterReviewView,
)


urlpatterns = [
    path(
        "property/<int:booking_id>/",
        PropertyRatingView.as_view(),
        name="property_rating",
    ),
    path("renter/<int:booking_id>/", RenterRatingView.as_view(), name="renter_rating"),
    path(
        "property-review/<int:booking_id>/",
        PropertyReviewView.as_view(),
        name="property_review",
    ),
    path(
        "renter-review/<int:booking_id>/",
        RenterReviewView.as_view(),
        name="renter_review",
    ),
]
