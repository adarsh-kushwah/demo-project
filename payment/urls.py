from django.urls import path, include
from django.contrib.auth import views as auth_views
from payment.views import (
    BookingBillView,
    AllBookingBillView,
    PayBillView,
    create_checkout_session,
    
)
from django.views.generic.base import TemplateView

urlpatterns = [
    path("all-bills/", AllBookingBillView.as_view(), name="all_bills"),
    path("bills/<int:booking_id>/", BookingBillView.as_view(), name="booking_bills"),
    path("pay-bill/<int:bill_id>/", PayBillView.as_view(), name="pay_bill"),
    path(
        "api/checkout-session/<int:bill_id>/",
        create_checkout_session,
        name="api_checkout_session",
    ),
    path(
        "payment-success/",
        TemplateView.as_view(template_name="payment/payment_success.html"),
        name="payment_success",
    ),
    path(
        "payment-fail/",
        TemplateView.as_view(template_name="payment/payment_fail.html"),
        name="payment_fail",
    ),
]
