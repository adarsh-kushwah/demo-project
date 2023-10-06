from django.urls import path
from django.contrib.auth import views as auth_views

from user.views import SignupView
from user.forms import UserProfileModelForm, AddressModelForm


urlpatterns = [
    path(
        "login/", auth_views.LoginView.as_view(next_page="/property/home/", template_name="user/login.html", extra_context={"address_form": AddressModelForm(),"profile_form": UserProfileModelForm(),}), name="login"
    ),
    path("signup/", SignupView.as_view(), name="signup"),
]