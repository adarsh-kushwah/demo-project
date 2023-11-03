from typing import Any

from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import DateInput
from django.shortcuts import render, redirect
from django.http import JsonResponse

from user.forms import UserProfileModelForm, AddressModelForm
from user.models import Location, UserProfile
from user.mixins import LogoutIfAuthenticatedMixin, UserAccessMixin


class SignupView(LogoutIfAuthenticatedMixin, View):
    """
    signup view for owner and renter
    """

    def get(self, request, *args, **kwargs):
        # ajax request when user select state and city
        if "state" in request.GET:
            state = request.GET.get("state")
            city_list = [
                (location.city, location.city)
                for location in Location.objects.filter(state__iexact=state)
                .distinct("city")
                .order_by("city")
            ]
            return JsonResponse({"choice_list": city_list}, status=200)

        elif "city" in request.GET:
            state = request.GET.get("city")
            postal_code_list = [
                (location.postal_code, location.postal_code)
                for location in Location.objects.filter(city__iexact=state)
            ]
            return JsonResponse({"postal_code_list": postal_code_list}, status=200)

        context = {
            "address_form": AddressModelForm(),
            "profile_form": UserProfileModelForm(),
        }
        return render(request, "user/signup.html", context)

    def post(self, request, *args, **kwargs):
        address_form = AddressModelForm(request.POST)
        profile_form = UserProfileModelForm(request.POST, request.FILES)

        if profile_form.is_valid() and address_form.is_valid():
            postal_code = address_form.cleaned_data["postal_code"]
            location = Location.objects.get(postal_code__iexact=postal_code)
            profile = profile_form.save()
            address_form.instance.location = location
            address_form.instance.user = profile
            address_form.save()
            return redirect(reverse("login"))
        else:
            print(profile_form.errors, address_form.errors)

        context = {"address_form": address_form, "profile_form": profile_form}
        return render(request, "user/signup.html", context)


class ViewProfile(LoginRequiredMixin, UserAccessMixin, DetailView):
    """
    user and renter can view their profile
    """

    pk_url_kwarg = "user_id"
    login_url = reverse_lazy("login")
    model = UserProfile


class UpdateProfile(LoginRequiredMixin, UserAccessMixin, UpdateView):
    pk_url_kwarg = "user_id"
    login_url = reverse_lazy("login")
    model = UserProfile
    template_name = "user/userprofile_detail.html"
    fields = [
        "username",
        "first_name",
        "last_name",
        "email",
        "date_of_birth",
        "gender",
        "marital_status",
        "profile_picture",
        "phone_number",
        "alternate_phone_number",
    ]

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields["date_of_birth"].widget = DateInput(attrs={"type": "date"})
        return form

    def get_success_url(self):
        return reverse("profile", kwargs={"user_id": self.request.user.id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["update_profile"] = True
        return context
