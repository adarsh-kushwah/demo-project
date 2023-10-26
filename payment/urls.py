from django.urls import path, include
from django.contrib.auth import views as auth_views
from payment.views import BookingBillView, AllBookingBillView, TestPayment, create_checkout_session


urlpatterns = [
    path('all-bills/',AllBookingBillView.as_view(),name="all_bills"),
    path("bills/<int:booking_id>/", BookingBillView.as_view(), name="booking_bills"),
    path('test/',TestPayment.as_view(),name="test"),
    path('api/checkout-session/', create_checkout_session, name='api_checkout_session'),
]
