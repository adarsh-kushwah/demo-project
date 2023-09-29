from django.urls import path
from property.views import Home
urlpatterns = [
    path("home/", Home.as_view(), name="home"),
]
