from django.urls import path
from property.views import Home, PostPropertyView, PropertyView, PropertyDetailView, PropertyRequestList, ApproveOrCancelRequest, BookingList, UpdateRequest


urlpatterns = [
    path("home/", Home.as_view(), name="home"),
    path("post/", PostPropertyView.as_view(), name="post_property"),
    path("update/<int:pk>/", PropertyView.as_view(), name="property"),
    path("detail/<int:pk>/", PropertyDetailView.as_view(), name='property_detail'),
    path("request/", PropertyRequestList.as_view(), name='property_request'),
    path("approve-or-reject-request/<int:pk>/", ApproveOrCancelRequest.as_view(), name='approve_or_reject_request'),
    path("booking/", BookingList.as_view(), name='rented'),
    path("update-request/<int:pk>/", UpdateRequest.as_view(), name='update_view'),
]
