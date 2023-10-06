from django.urls import path
from property.views import Home, PostPropertyView, PropertyView, PropertyDetailView, PropertyRequestList

urlpatterns = [
    path("home/", Home.as_view(), name="home"),
    path("post/", PostPropertyView.as_view(), name="post_property"),
    path("update/<int:pk>/", PropertyView.as_view(), name="property"),
    path("detail/<int:pk>/", PropertyDetailView.as_view(), name='property_detail'),
    path("request/", PropertyRequestList.as_view(), name='property_request'),
]
