from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.views import View
from django.http import JsonResponse

from rating.models import PropertyRating, RenterRating

from property.models import Booking
from user.models import UserProfile

class PropertyRatingView( View):
    login_url = "/user/login/"
    
    def post(self, request, *args, **kwargs):
        
        booking_id = self.kwargs['booking_id']
        rating = request.POST.get('star',0)
        booking = Booking.objects.get(id=booking_id)
        user = UserProfile.objects.get(id = request.user.id)
        property_rating = PropertyRating.objects.filter(renter=user,
                                       property=booking.property_request_response.property,
                                       booking = booking)
        if property_rating.exists():
            property_rating = property_rating.first()
            property_rating.rating = rating
            property_rating.save()
        else:
            PropertyRating.objects.create(renter=user,
                                       property=booking.property_request_response.property,
                                       booking = booking,
                                       rating=rating)
        return JsonResponse({})


class RenterRatingView( View):
    login_url = "/user/login/"
    
    def post(self, request, *args, **kwargs):
        
        booking_id = self.kwargs['booking_id']
        rating = request.POST.get('star',0)
        booking = Booking.objects.get(id=booking_id)
        renter = booking.renter
        user = UserProfile.objects.get(id = request.user.id)
        property_rating = RenterRating.objects.filter(owner=user,
                                        renter = renter,
                                        property= booking.property_request_response.property,
                                        booking = booking)
        if property_rating.exists():
            property_rating = property_rating.first()
            property_rating.rating = rating
            property_rating.save()
        else:
            RenterRating.objects.create(
                                        owner = user,
                                        renter=renter,
                                        property=booking.property_request_response.property,
                                        booking = booking,
                                        rating=rating)
        return JsonResponse({})


