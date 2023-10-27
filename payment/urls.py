from django.urls import path, include
from django.contrib.auth import views as auth_views
from payment.views import BookingBillView, AllBookingBillView, PayBillView, TestPayment, create_checkout_session, PaymentSuccessView


urlpatterns = [
    path('all-bills/',AllBookingBillView.as_view(),name="all_bills"),
    path("bills/<int:booking_id>/", BookingBillView.as_view(), name="booking_bills"),
    path('pay-bill/<int:bill_id>/',PayBillView.as_view(),name="pay_bill"),
    path('test/',TestPayment.as_view(),name="test"),
    path('api/checkout-session/<int:bill_id>/', create_checkout_session, name='api_checkout_session'),
    path('payment-success/<int:bill_id>/',PaymentSuccessView.as_view(),name="payment_success"),
]
