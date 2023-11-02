from django.urls import path
from property.views import (
    Home,
    PostPropertyView,
    UpdatePropertyView,
    PropertyDetailView,
    PropertyRequestList,
    RequestResponseView,
    BookingList,
    UpdateRequest,
    LeaveProperty,
    UpdateRequestResponseView,
    ConfirmBookingView,
    GenerateAgreementPdfView,
)


urlpatterns = [
    path("home/", Home.as_view(), name="home"),
    path("post/", PostPropertyView.as_view(), name="post_property"),
    path("update/<int:pk>/", UpdatePropertyView.as_view(), name="update_property"),
    path("detail/<int:pk>/", PropertyDetailView.as_view(), name="property_detail"),
    path("requests/", PropertyRequestList.as_view(), name="property_requests"),
    path(
        "request-response/<int:pk>/",
        RequestResponseView.as_view(),
        name="request_response",
    ),
    path("bookings/", BookingList.as_view(), name="bookings"),
    path("update-request/<int:pk>/", UpdateRequest.as_view(), name="update_view"),
    path("leave/<int:pk>/", LeaveProperty.as_view(), name="leave_property"),
    path(
        "update-request-response/<int:pk>/",
        UpdateRequestResponseView.as_view(),
        name="update_request_response",
    ),
    path(
        "confirm-booking/<int:pk>/",
        ConfirmBookingView.as_view(),
        name="confirm_booking",
    ),
    path(
        "generate-agreement-pdf/<int:property_request_id>/",
        GenerateAgreementPdfView.as_view(),
        name="agreement_pdf",
    ),
]
