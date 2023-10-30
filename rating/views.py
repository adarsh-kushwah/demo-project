from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse

from rating.models import PropertyRating, RenterRating, PropertyReview, RenterReview
from rating.forms import PropertyReviewModelForm, RenterReviewModelForm

from property.models import Booking
from user.models import UserProfile


class PropertyRatingView(View):
    login_url = "/user/login/"

    def post(self, request, *args, **kwargs):
        booking_id = self.kwargs["booking_id"]
        rating = request.POST.get("star", 0)
        booking = Booking.objects.get(id=booking_id)
        user = UserProfile.objects.get(id=request.user.id)
        property_rating = PropertyRating.objects.filter(booking=booking)
        if property_rating.exists():
            property_rating = property_rating.first()
            property_rating.rating = rating
            property_rating.save()
        else:
            PropertyRating.objects.create(
                renter=user,
                property=booking.property_request_response.request_response_property,
                booking=booking,
                rating=rating,
            )
        return JsonResponse({})


class RenterRatingView(View):
    login_url = "/user/login/"

    def post(self, request, *args, **kwargs):
        booking_id = self.kwargs["booking_id"]
        rating = request.POST.get("star", 0)
        booking = Booking.objects.get(id=booking_id)
        renter = booking.renter
        user = UserProfile.objects.get(id=request.user.id)
        renter_rating = RenterRating.objects.filter(booking=booking)
        if renter_rating.exists():
            renter_rating = renter_rating.first()
            renter_rating.rating = rating
            renter_rating.save()
        else:
            RenterRating.objects.create(
                owner=user,
                renter=renter,
                property=booking.property_request_response.request_response_property,
                booking=booking,
                rating=rating,
            )
        return JsonResponse({})


class PropertyReviewView(View):
    login_url = "/user/login/"

    def post(self, request, *args, **kwargs):
        booking_id = self.kwargs["booking_id"]
        booking = Booking.objects.get(id=booking_id)
        property_review = PropertyReview.objects.filter(booking=booking)

        if property_review.exists():
            property_review_form = PropertyReviewModelForm(
                request.POST, instance=property_review.first()
            )
        else:
            property_review_form = PropertyReviewModelForm(request.POST)

        context = {}
        if property_review_form.is_valid():
            property_review_form.instance.booking = booking
            property_review_form.instance.renter = booking.renter
            property_review_form.instance.property = (
                booking.property_request_response.property
            )
            property_review_form.save()
            context["description"] = property_review_form.cleaned_data["description"]
        else:
            print("invalid----->", property_review_form.errors)
        return JsonResponse(context)


class RenterReviewView(View):
    def post(self, request, *args, **kwargs):
        booking_id = self.kwargs["booking_id"]
        booking = Booking.objects.get(id=booking_id)
        renter_review = RenterReview.objects.filter(booking=booking)

        if renter_review.exists():
            renter_review_form = RenterReviewModelForm(
                request.POST, instance=renter_review.first()
            )
        else:
            renter_review_form = RenterReviewModelForm(request.POST)

        context = {}
        if renter_review_form.is_valid():
            user = UserProfile.objects.get(id=request.user.id)
            renter_review_form.instance.booking = booking
            renter_review_form.instance.renter = booking.renter
            renter_review_form.instance.property = (
                booking.property_request_response.request_response_property
            )
            renter_review_form.instance.owner = user
            renter_review_form.save()
            context["description"] = renter_review_form.cleaned_data["description"]
        else:
            print("invalid----->", renter_review_form.errors)
        return JsonResponse(context)
