from typing import Any
import os
import json

from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django import forms
from django.core.paginator import Paginator
from django.db.models import Q, Subquery, Avg
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden, JsonResponse, HttpResponse, QueryDict

from user.models import UserProfile

from property.models import (
    Booking,
    PropertyImage,
    Property,
    PropertyRequestResponse,
    Amenity,
)
from property.forms import (
    PropertyForm,
    AddressModelForm,
    ProprtyImageModelForm,
    RequestPropertyModelForm,
    PropertyRequestResponseForm,
    AgreementModelForm,
)

from rating.forms import PropertyReviewModelForm, RenterReviewModelForm

from payment.utility import generate_pdf

from property.mixins import ProperetyAccessMixin

from property.tasks import testing_celery


class Home(View):
    """
    Home view showing properties according to authenticated user
    User:-
        Authenticated user -
            Owner - allow to view and edit his property
            Renter - allow to view all properties and can request property
        Anonymous user -
            can see all the properties but not have access to see detail and request property
    """

    template_name = "property/home.html"
    property_per_page = 2

    def get(self, request, *args, **kwargs):
        context = {}

        if not request.user.is_anonymous:
            user = UserProfile.objects.get(username=request.user.username)
            context["user"] = user
            if user.user_type == "owner":
                context["property"] = (
                    user.property_set.all()
                    .annotate(rating=Avg("propertyrating__rating", default=0))
                    .order_by("created_at")
                )

            else:
                context["property"] = (
                    Property.objects.filter(is_available=True)
                    .annotate(rating=Avg("propertyrating__rating", default=0))
                    .order_by("created_at")
                )

        else:
            context["property"] = (
                Property.objects.filter(is_available=True)
                .annotate(rating=Avg("propertyrating__rating", default=0))
                .order_by("created_at")
            )

        if "search" in request.GET:
            search_value = request.GET.get("search")
            context["property"] = context["property"].filter(
                Q(name__icontains=search_value)
                | Q(propertyaddress__street_address__icontains=search_value)
                | Q(propertyaddress__location__city__icontains=search_value)
            )
            context["search"] = search_value

        if "min_price" and "max_price" in request.GET:
            min_price = request.GET.get("min_price")
            max_price = request.GET.get("max_price")
            context["property"] = context["property"].filter(
                rent_amount__range=[min_price, max_price]
            )
            context["min_price"] = min_price
            context["max_price"] = max_price

        if "property_type" in request.GET:
            property_type = request.GET.get("property_type")
            if property_type != "all":
                context["property"] = context["property"].filter(
                    property_type__exact=property_type
                )
            context["property_type"] = property_type

        paginated_list = Paginator(context["property"], self.property_per_page)
        page_number = request.GET.get("page", 1)
        page_obj = paginated_list.get_page(page_number)

        context["property"] = page_obj

        result = testing_celery.delay(4,5)
        if result.ready():
            print('--->ready result',result.result)
        print('celery--->',result)
        print('--->><>ccele')
        return render(request, self.template_name, context)


class PostPropertyView(LoginRequiredMixin, View):
    """
    Owner can Post new property
    """

    login_url = reverse_lazy("login")
    amenity_model_formset = forms.modelformset_factory(
        Amenity, fields=["name", "status"]
    )

    def get(self, request, *args, **kwargs):
        property_form = PropertyForm(initial={"owner": request.user})
        context_data = {
            "property_form": property_form,
            "address_form": AddressModelForm(),
            "proprty_image_form": ProprtyImageModelForm(),
            "amenity_form": self.amenity_model_formset(queryset=Amenity.objects.none()),
        }
        return render(request, "property/post_property.html", context_data)

    def post(self, request, *args, **kwargs):
        property_form = PropertyForm(request.POST)
        address_form = AddressModelForm(request.POST)
        proprty_image_form_set = ProprtyImageModelForm(request.POST, request.FILES)
        amenity_form_set = self.amenity_model_formset(request.POST)

        if (
            address_form.is_valid()
            and property_form.is_valid()
            and proprty_image_form_set.is_valid()
            and amenity_form_set.is_valid()
        ):
            location = address_form.cleaned_data["postal_code"]
            property = property_form.save()
            address_form.instance.location = location
            address_form.instance.property = property
            address_form.save()
            image_files = request.FILES.getlist("image")

            for img in image_files:
                """
                storing multiple images of property (bulkcreate use)
                """
                PropertyImage.objects.create(property=property, image=img)

            for form in amenity_form_set:
                if form.is_valid():
                    form.instance.property = property
                    form.save()
                else:
                    print("not valid", form.errors)

            return redirect(reverse("home"))
        else:
            print(
                address_form.errors,
                proprty_image_form_set.errors,
                property_form.errors,
                amenity_form_set.errors,
            )
        context_data = {
            "property_form": property_form,
            "address_form": address_form,
            "proprty_image_form": proprty_image_form_set,
            "amenity_form": amenity_form_set,
        }
        return render(request, "property/post_property.html", context_data)


class UpdatePropertyView(LoginRequiredMixin, ProperetyAccessMixin, View):
    """
    owner can update property
    """

    login_url = reverse_lazy("login")
    template_name = "property/update_property.html"
    amenity_model_formset = forms.modelformset_factory(
        Amenity, fields=["name", "status"], extra=0
    )

    def get(self, request, *args, **kwargs):
        property = get_object_or_404(Property, pk=kwargs["property_id"])
        if property.propertyaddress.location:
            postal_code = property.propertyaddress.location.postal_code
        else:
            postal_code = 'not available'
        context_data = {
            "property": property,
            "property_form": PropertyForm(instance=property),
            "address_form": AddressModelForm(
                instance=property.propertyaddress, initial={"postal_code": postal_code}
            ),
            "proprty_image_form": ProprtyImageModelForm(),
            "amenity_form": self.amenity_model_formset(
                queryset=Amenity.objects.filter(property=property)
            ),
        }
        return render(request, self.template_name, context_data)

    def post(self, request, *args, **kwargs):
        property = get_object_or_404(Property, pk=kwargs["property_id"])
        proprty_image_form = ProprtyImageModelForm(request.POST, request.FILES)
        property_form = PropertyForm(request.POST, instance=property)
        address_form = AddressModelForm(request.POST, instance=property.propertyaddress)
        amenity_form_set = self.amenity_model_formset(
            request.POST, queryset=Amenity.objects.filter(property=property)
        )

        if "updateImage" in request.POST:
            if proprty_image_form.is_valid():
                image_files = request.FILES.getlist("image")

                for img in image_files:
                    """
                    storing multiple images of property
                    """
                    PropertyImage.objects.create(property=property, image=img)
                return redirect(reverse("home"))

        else:
            if (
                address_form.is_valid()
                and property_form.is_valid()
                and amenity_form_set.is_valid()
            ):
                property_form.save()
                address_form.instance.location = address_form.cleaned_data[
                    "postal_code"
                ]
                address_form.save()

                for form in amenity_form_set:
                    if form.is_valid():
                        form.instance.property = property
                        form.save()
                    else:
                        print("not valid", form.errors)
                return redirect(reverse("home"))
            else:
                print(
                    "eerroe",
                    property_form.errors,
                    address_form.errors,
                    amenity_form_set.errors,
                )

        context_data = {
            "property": property,
            "property_form": property_form,
            "address_form": address_form,
            "proprty_image_form": proprty_image_form,
            "message": "Update Property",
        }
        return render(request, self.template_name, context_data)

    def delete(self, request, *args, **kwargs):
        data = QueryDict(request.body)
        request_type = data.get("request_type", None)

        if request_type == "delete_property_image":
            image_id = kwargs["pk"]
            property_image = PropertyImage.objects.get(id=image_id)
            property_image.delete()
            return JsonResponse({})


class PropertyDetailView(LoginRequiredMixin, DetailView):
    pk_url_kwarg = "property_id"
    login_url = reverse_lazy("login")
    model = Property
    """
        GET :- Detail of selected property with Request Property Form

        POST :- Renter can send request for selected property
    """

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
            property = get_object_or_404(Property, pk=kwargs["property_id"])
            user = get_object_or_404(UserProfile, id=request.user.id)
            request_property_form.instance.user = user
            request_property_form.instance.request_response_property = property
            request_property_form.save()
            return redirect(reverse("property_requests"))


class UpdateRequest(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy("login")
    model = PropertyRequestResponse
    fields = ["start_date", "end_date", "rent_amount"]
    template_name = "property/update_request.html"
    request_response_status = PropertyRequestResponse.STATUS_CHOICES

    """
        Renter can update the request to the property untill Owner Responsed

        POST :- Renter can update request untill Owner Responsed,
                if owner Rejected request then renter can also resend request
    """

    def get_success_url(self):
        return reverse_lazy("property_requests")

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
        request_type = request.GET.get("request_type", None)

        if request_type == "resend_request":
            property_request = get_object_or_404(
                PropertyRequestResponse, pk=kwargs["pk"]
            )
            property_request.status = self.request_response_status[0][0]
            # status = "processing"
            property_request.save()

        return super(UpdateRequest, self).post(request, **kwargs)


class PropertyRequestList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy("login")
    model = PropertyRequestResponse
    template_name = "property/request_list.html"
    user_type_choices = UserProfile.USER_TYPE_CHOICES
    request_response_status = PropertyRequestResponse.STATUS_CHOICES
    """
        Showing all Renter's Requests for Property to owner 
    """

    def get_queryset(self):
        user_id = self.request.user.id
        # user_type = "owner"
        if self.request.user.user_type == self.user_type_choices[1][0]:
            # status =  "processing" |"responsed"
            # user_type = "renter"
            queryset = self.model.objects.filter(
                Q(status=self.request_response_status[0][0])
                | Q(status=self.request_response_status[1][0]),
                request_response_property__owner__id=user_id,
                user__user_type=self.user_type_choices[0][0],
            ).annotate(rating=Avg("request_response_property__renterrating__rating"))
        else:
            # status =  "processing" |"responsed" | rejected""
            queryset = self.model.objects.filter(
                Q(status=self.request_response_status[0][0])
                | Q(status=self.request_response_status[1][0])
                | Q(status=self.request_response_status[2][0]),
                user_id=user_id,
            ).distinct("request_response_property")
        return queryset


class RequestResponseView(LoginRequiredMixin, View):
    login_url = reverse_lazy("login")
    template_name = "property/request_detail.html"
    request_response_status = PropertyRequestResponse.STATUS_CHOICES
    """
        GET :- Owner can response to Renter's request
            Showing PropertyRequestResponse form 
            If owner responded to renter's request then initial data to the form will be the responded values, and if owner not responded then initail data will be renter's requested values
        
        POST :- Owner can response to renter's request
    """

    def get(self, request, *args, **kwargs):
        property_request_id = kwargs["pk"]
        property_request = get_object_or_404(
            PropertyRequestResponse, pk=property_request_id
        )
        request_response = PropertyRequestResponse.objects.filter(
            request_token=property_request.request_token
        ).last()

        context = {
            "property_request": property_request,
            "request_response": request_response,
        }
        if request_response.status == self.request_response_status[1][0]:
            # for responsed requests
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
        return render(request, self.template_name, context)

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
            property_request_response_form.instance.request_response_property = (
                property_request.request_response_property
            )
            property_request_response_form.save()
            PropertyRequestResponse.objects.filter(request_token=request_token).update(
                status=self.request_response_status[1][0]
            )
            # here status = responsed
            return redirect(reverse("home"))

    def delete(self, request, *args, **kwargs):
        property_request_id = kwargs["pk"]
        property_request = get_object_or_404(
            PropertyRequestResponse, pk=property_request_id
        )
        reject_request = request.GET.get("reject_request", None)
        if reject_request:
            if reject_request == "owner":
                PropertyRequestResponse.objects.filter(
                    request_token=property_request.request_token
                ).update(status=self.request_response_status[2][0])
            else:
                PropertyRequestResponse.objects.filter(
                    request_token=property_request.request_token
                ).delete()
            return JsonResponse({"status": "success"})

        return JsonResponse({"status": "success"})


class GenerateAgreementPdfView(View):
    """
    generating pdf aggrement between owner and renter
    """

    def get(self, request, *args, **kwargs):
        property_request_id = kwargs["property_request_id"]
        property_request = get_object_or_404(
            PropertyRequestResponse, pk=property_request_id
        )
        request_response = PropertyRequestResponse.objects.filter(
            request_token=property_request.request_token
        ).last()

        context = {
            "property_request": property_request,
            "request_response": request_response,
        }
        pdf = generate_pdf(request, "property/generate_agreement_pdf.html", context)
        response = HttpResponse(pdf, content_type="application/pdf")
        response["Content-Disposition"] = 'filename="rental-agreement.pdf"'
        return response


class UpdateRequestResponseView(LoginRequiredMixin, UpdateView):
    """
    Owner can update the renter's request response
    """

    login_url = reverse_lazy("login")
    model = PropertyRequestResponse
    fields = ["rent_amount", "start_date", "end_date"]

    def get_success_url(self):
        return reverse_lazy("property_requests")


class ConfirmBookingView(LoginRequiredMixin, View):
    """
    Renter confirm the booking after owner's response on request
    """

    login_url = reverse_lazy("login")
    request_response_status = PropertyRequestResponse.STATUS_CHOICES

    def post(self, request, *args, **kwargs):
        property_request_response_id = kwargs["pk"]
        agreement_form = AgreementModelForm(request.POST, request.FILES)
        if agreement_form.is_valid():
            property_request_response = get_object_or_404(
                PropertyRequestResponse, pk=property_request_response_id
            )
            property = property_request_response.request_response_property
            booking = Booking.objects.create(
                property_request_response=property_request_response
            )

            agreement_form.instance.booking = booking
            property.is_available = False
            PropertyRequestResponse.objects.filter(
                request_token=property_request_response.request_token
            ).update(status=self.request_response_status[3][0])
            # status = approved
            agreement_form.save()
            property.save()

            return redirect("bookings")
        else:
            print("--------->", agreement_form.errors)


class BookingList(LoginRequiredMixin, ListView):
    """
    showing current and history booking lists
    """

    login_url = reverse_lazy("login")
    model = Booking
    request_response_status = PropertyRequestResponse.STATUS_CHOICES

    def get_queryset(self):
        user_id = self.request.user.id

        quertset = self.model.objects.filter(
            property_request_response__request_token__in=Subquery(
                PropertyRequestResponse.objects.filter(
                    user__id=user_id, status=self.request_response_status[3][0]
                ).values("request_token")
            ),
        ).order_by("created_at")
        # status = approved
        return quertset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.request.user.id

        context["booking_history_list"] = self.model.objects.filter(
            property_request_response__request_token__in=Subquery(
                PropertyRequestResponse.objects.filter(
                    user__id=user_id,
                    status=self.request_response_status[4][0],
                ).values("request_token")
            ),
        ).order_by("created_at")
        # status = left
        context["property_review_form"] = PropertyReviewModelForm()
        context["renter_review_form"] = RenterReviewModelForm()

        return context


class LeaveProperty(LoginRequiredMixin, View):
    """
    when owner leave property
    """

    request_response_status = PropertyRequestResponse.STATUS_CHOICES

    def get(self, request, *args, **kwargs):
        property = get_object_or_404(Property, pk=kwargs["pk"])
        PropertyRequestResponse.objects.filter(
            request_response_property=property
        ).update(status=self.request_response_status[4][0])
        # status left
        property.is_available = True
        property.save()
        return redirect(reverse("home"))
