from typing import Any
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.forms import formset_factory
from django.db.models import Q
from django import forms
from django.urls import reverse_lazy


from user.models import UserProfile
from property.models import (
    Booking,
    PropertyImage,
    Property,
    Agreement,
    PropertyRequestResponse,
)
from property.forms import (
    PropertyForm,
    AddressModelForm,
    ProprtyImageModelForm,
    RequestPropertyModelForm,
    PropertyRequestResponseForm,
    AgreementModelForm,
)

import os


class Home(View):
    def get(self, request, *args, **kwargs):
        context = {}
        if not request.user.is_anonymous:
            user = UserProfile.objects.get(username=request.user.username)
            context["user"] = user
            if user.user_type == "owner":
                context["property"] = user.property_set.all()
            else:
                context["property"] = Property.objects.filter(is_available=True)
        else:
            context["property"] = Property.objects.filter(is_available=True)

        return render(request, "property/home.html", context)


class PostPropertyView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, *args, **kwargs):
        property_form = PropertyForm(initial={"owner": request.user})
        context_data = {
            "property_form": property_form,
            "address_form": AddressModelForm(),
            "proprty_image_form": ProprtyImageModelForm(),
        }
        return render(request, "property/post_property.html", context_data)

    def post(self, request, *args, **kwargs):
        property_form = PropertyForm(request.POST)
        address_form = AddressModelForm(request.POST)
        proprty_image_form = ProprtyImageModelForm(request.POST, request.FILES)
        if (
            address_form.is_valid()
            and property_form.is_valid()
            and proprty_image_form.is_valid()
        ):
            location = address_form.cleaned_data["postal_code"]
            property = property_form.save()
            proprty_image_form.instance.property = property
            proprty_image_form.save()
            address_form.instance.location = location
            address_form.instance.property = property
            address_form.save()
            return redirect(reverse("home"))
        else:
            print(
                address_form.errors,
                proprty_image_form.errors,
                property_form.errors,
            )
        context_data = {
            "property_form": property_form,
            "address_form": address_form,
            "proprty_image_form": proprty_image_form,
        }
        return render(request, "property/post_property.html", context_data)


class PropertyView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, *args, **kwargs):
        property_id = kwargs["pk"]
        property = get_object_or_404(Property, pk=property_id)
        postal_code = property.propertyaddress.location.postal_code
        context_data = {
            "property": property,
            "property_form": PropertyForm(instance=property),
            "address_form": AddressModelForm(
                instance=property.propertyaddress, initial={"postal_code": postal_code}
            ),
            "proprty_image_form": ProprtyImageModelForm(),
        }
        return render(request, "property/update_property.html", context_data)

    def post(self, request, *args, **kwargs):
        property_id = kwargs["pk"]
        property = get_object_or_404(Property, pk=property_id)
        property_image = property.propertyimage_set.first()
        proprty_image_form = ProprtyImageModelForm(
            request.POST, request.FILES, instance=property_image
        )
        proprty_image_form = ProprtyImageModelForm(
            request.POST, request.FILES, instance=property_image
        )
        property_form = PropertyForm(request.POST, instance=property)
        address_form = AddressModelForm(request.POST, instance=property.propertyaddress)

        if "updateImage" in request.POST:
            if proprty_image_form.is_valid():
                image_path = property_image.image.path
                if os.path.exists(image_path):
                    os.remove(image_path)
                proprty_image_form.save()
                return redirect(reverse("home"))
        else:
            if address_form.is_valid() and property_form.is_valid():
                property_form.save()
                address_form.instance.location = address_form.cleaned_data[
                    "postal_code"
                ]
                address_form.save()
                return redirect(reverse("home"))
            else:
                print("eerroe", property_form.errors, address_form.errors)

        postal_code = property.propertyaddress.location.postal_code
        context_data = {
            "property": property,
            "property_form": property_form,
            "address_form": address_form,
            "proprty_image_form": proprty_image_form,
            "message": "Update Property",
        }
        return render(request, "property/update_property.html", context_data)


class PropertyDetailView(LoginRequiredMixin, DetailView):
    login_url = "/user/login/"
    model = Property

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        property = context["property"]
        initail_data = {"rent_amount": property.rent_amount}
        context["request_property_form"] = RequestPropertyModelForm(
            initial=initail_data
        )
        return context

    def post(self, request, *args, **kwargs):
        request_property_form = RequestPropertyModelForm(request.POST)

        if request_property_form.is_valid():
            property = get_object_or_404(Property, pk=kwargs["pk"])
            user = get_object_or_404(UserProfile, id=request.user.id)
            request_property_form.instance.user = user
            request_property_form.instance.property = property
            request_property_form.save()
            return redirect(reverse("property_request"))


class PropertyRequestList(LoginRequiredMixin, ListView):
    login_url = "/user/login/"
    model = PropertyRequestResponse
    template_name = "property/request_list.html"

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.user_type == "owner":
            queryset = self.model.objects.filter(
                Q(status="processing") | Q(status="responsed"),
                property__owner_id=user_id,
            ).distinct("property")
        else:
            queryset = self.model.objects.filter(
                ~Q(status="approved"), user_id=user_id
            ).distinct("property")
        return queryset

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     try:
    #         property_request_response = property_request.propertyrequestresponse
    #     except :
    #         property_request_response = None
    #     print('-------->',property_request_response)
    #     return context


class PropertyRequestResponseView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        property_request_id = kwargs["pk"]
        reject_request = request.GET.get("reject_request", None)
        property_request = get_object_or_404(
            PropertyRequestResponse, pk=property_request_id
        )
        if reject_request:
            if reject_request == "owner":
                property_request.status = "rejected"
                property_request.save()
            else:
                property_request.delete()
            return redirect(reverse("home"))
        request_response = PropertyRequestResponse.objects.filter(
            request_token=property_request.request_token
        ).last()

        context = {
            "property_request": property_request,
            "request_response": request_response,
        }
        if request_response.status == "responsed":
            inital_data = {
                "start_date": request_response.start_date,
                "end_date": request_response.end_date,
                "rent_amount": request_response.rent_amount,
                "request_token": request_response.request_token,
            }
        else:
            inital_data = {
                "start_date": property_request.start_date,
                "end_date": property_request.end_date,
                "rent_amount": property_request.rent_amount,
                "request_token": property_request.request_token,
            }
        property_request_response_form = PropertyRequestResponseForm(
            initial=inital_data
        )
        agreement_form = AgreementModelForm()

        context["request_response_form"] = property_request_response_form
        context["agreement_form"] = agreement_form
        return render(request, "property/request_detail.html", context)

    def post(self, request, *args, **kwargs):
        property_request_id = kwargs["pk"]
        property_request = get_object_or_404(
            PropertyRequestResponse, pk=property_request_id
        )
        user = get_object_or_404(UserProfile, pk=request.user.id)
        property_request_response_form = PropertyRequestResponseForm(
            request.POST, request.FILES
        )
        if property_request_response_form.is_valid():
            request_token = property_request_response_form.cleaned_data["request_token"]
            property_request_response_form.instance.user = user
            property_request_response_form.instance.property_request = property_request
            property_request_response_form.instance.property = property_request.property
            property_request_response_form.save()
            PropertyRequestResponse.objects.filter(request_token=request_token).update(
                status="responsed"
            )
            return redirect(reverse("home"))


class ConfirmBookingView(LoginRequiredMixin, View):
    """
    Renter confirm the booking after owner's response on request
    """

    login_url = "/user/login/"

    def post(self, request, *args, **kwargs):
        property_request_response_id = kwargs["pk"]
        agreement_form = AgreementModelForm(request.POST, request.FILES)
        if agreement_form.is_valid():
            property_request_response = get_object_or_404(
                PropertyRequestResponse, pk=property_request_response_id
            )
            property = property_request_response.property
            booking = Booking.objects.create(
                property_request_response=property_request_response
            )
            agreement_form.instance.booking = booking
            property.is_available = False
            PropertyRequestResponse.objects.filter(
                request_token=property_request_response.request_token
            ).update(status="approved")
            agreement_form.save()
            property.save()

            return redirect("bookings")
        else:
            print("--------->", agreement_form.errors)


class BookingList(LoginRequiredMixin, ListView):
    login_url = "/user/login/"
    model = Booking

    def get_queryset(self):
        user_id = self.request.user.id
        try:
            property_response = PropertyRequestResponse.objects.get(user__id=user_id)
        except:
            return Booking.objects.none()

        if self.request.user.user_type == "owner":
            queryset = self.model.objects.filter(
                property_request_response__property__owner__id=user_id,
                property_request_response__property__is_available=False,
            )
        else:
            property_request = PropertyRequestResponse.objects.get(
                request_token=property_response.request_token, user__id=user_id
            )
            queryset = self.model.objects.filter(
                property_request_response__request_token=property_request.request_token,
                property_request_response__property__is_available=False,
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id
        if self.request.user.user_type == "owner":
            context["booking_history_list"] = self.model.objects.filter(
                property_request_response__property__owner__id=user_id,
                property_request_response__property__is_available=True,
            )
        else:
            try:
                property_response = PropertyRequestResponse.objects.get(
                    user__id=user_id
                )
            except:
                return Booking.objects.none()

            property_request = PropertyRequestResponse.objects.get(
                request_token=property_response.request_token, user__id=user_id
            )
            context["booking_history_list"] = self.model.objects.filter(
                property_request_response__request_token=property_request.request_token,
                property_request_response__property__is_available=True,
            )
        return context


class UpdateRequest(LoginRequiredMixin, UpdateView):
    login_url = "/user/login/"
    model = PropertyRequestResponse
    fields = ["start_date", "end_date", "rent_amount"]
    template_name = "property/update_request.html"
    success_url = "/property/request/"

    def get_form_class(self):
        form_class = super().get_form_class()
        form_class.base_fields["start_date"].widget = forms.widgets.DateInput(
            attrs={"type": "date"}
        )
        form_class.base_fields["end_date"].widget = forms.widgets.DateInput(
            attrs={"type": "date"}
        )
        return form_class

    def post(self, request, *args, **kwargs):
        if "request_type" in request.GET:
            property_request = get_object_or_404(
                PropertyRequestResponse, pk=kwargs["pk"]
            )
            property_request.status = "processing"
            property_request.save()

        return super(UpdateRequest, self).post(request, **kwargs)


class UpdateRequestResponseView(LoginRequiredMixin, UpdateView):
    """
    Renter update the property request
    """

    login_url = "/user/login/"
    model = PropertyRequestResponse
    fields = ["rent_amount", "start_date", "end_date"]
    # success_url = "/property/property-request-response/"
    success_url = "/property/request/"

    # def get_success_url(self):
    #     return reverse_lazy('property_request_response', kwargs={'pk': self.object.property_request.id})


class LeaveProperty(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        user = UserProfile.objects.get(username=request.user.username)
        property_id = kwargs["pk"]
        property = get_object_or_404(Property, pk=kwargs["pk"])
        property.is_available = True
        property.save()
        return redirect(reverse("home"))
