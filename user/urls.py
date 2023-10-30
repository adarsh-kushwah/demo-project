from django.urls import path, include
from django.contrib.auth import views as auth_views

from user.views import SignupView, ViewProfile, UpdateProfile
from user.forms import UserProfileModelForm, AddressModelForm


urlpatterns = [
    path(
        "login/",
        auth_views.LoginView.as_view(
            next_page="/property/home/", template_name="user/login.html"
        ),
        name="login",
    ),
    path("signup/", SignupView.as_view(), name="signup"),
    path("profile/<int:user_id>/", ViewProfile.as_view(), name="profile"),
    path(
        "update-profile/<int:user_id>/", UpdateProfile.as_view(), name="update_profile"
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(next_page="/user/login/"),
        name="logout",
    ),
    path(
        "change-password/",
        auth_views.PasswordChangeView.as_view(
            success_url="/user/login/", template_name="user/change_password.html"
        ),
        name="change_password",
    ),
    path("", include("django.contrib.auth.urls")),
]
