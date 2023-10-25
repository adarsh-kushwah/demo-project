from django.urls import path, include
from django.contrib.auth import views as auth_views
from payment.views import GenerateBillView, BookingBillView, AllBookingBillView


urlpatterns = [
    path("generate-bill/", GenerateBillView.as_view(), name="property_rating"),
    path('all-bills/',AllBookingBillView.as_view(),name="all_bills"),
    path("bills/<int:booking_id>/", BookingBillView.as_view(), name="booking_bills"),
]
