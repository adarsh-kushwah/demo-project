from django.shortcuts import render
# from django.views.generic.base import TemplateView
# Create your views here.
from django.views import View
from user.models import UserProfile
from property.models import Booking

class Home(View):

    def get(self, request, *args, **kwargs):
        context ={}
        if request.user.is_authenticated():
            user = UserProfile.objects.get(username = request.user.username)
            booking = Booking.objects.all()
            if user.user_type == 'owner':   
                property = user.property_set.all()
                if property.exists() :
                    context['total_property'] = property.count()
                    context['total_property_for_rent'] = property.filter(is_active=True).count()
                    context['total_property_rented'] = property.filter(is_available=False).count()
                    context['total_pending_requests'] = booking.filter(is_approved=False ,property__owner=user).count()
            else :
                context['total_property_on_rent'] = booking.filter(user=user, is_approved=True).count()
                context['total_property_requests'] = booking.filter(user=user, is_approved=False).count()
        return render(request, "property/home.html", context)
    

class Property(View):

    def get(self, request, *args, **kwargs):
        pass