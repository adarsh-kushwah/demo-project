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

from user.models import UserProfile
from property.models import Booking, PropertyImage, Property, PropertyRequest, Agreement
from property.forms import PropertyForm, AddressModelForm, ProprtyImageModelForm, RequestPropertyModelForm, ApproveRequestForm

import os


class Home(View):

    def get(self, request, *args, **kwargs):
        context ={}
        if not request.user.is_anonymous:
            user = UserProfile.objects.get(username = request.user.username)

            if user.user_type == 'owner':
                context['property'] = user.property_set.all()
            else:
                context['property'] = Property.objects.all()
        else:
            context['property'] = Property.objects.all()

        return render(request, "property/home.html", context)
    

class PostPropertyView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, *args, **kwargs):
        property_form = PropertyForm(initial = {"owner":request.user})
        context_data = {'property_form':property_form,'address_form':AddressModelForm(),'proprty_image_form':ProprtyImageModelForm()}
        print('--',property_form)
        return render(request, "property/post_property.html", context_data)

    def post(self, request, *args, **kwargs):
        property_form = PropertyForm(request.POST)
        address_form = AddressModelForm(request.POST)
        proprty_image_form = ProprtyImageModelForm(request.POST, request.FILES)
        if address_form.is_valid() and property_form.is_valid() and proprty_image_form.is_valid() :
            location = address_form.cleaned_data["postal_code"]
            property = property_form.save()
            proprty_image_form.instance.property = property
            proprty_image_form.save()
            address_form.instance.location = location
            address_form.instance.property = property
            address_form.save()         
            return redirect(reverse('home'))
        else:
            print('------>',address_form.errors,proprty_image_form.errors,property_form.errors)
        context_data = {'property_form':property_form,'address_form':address_form,'proprty_image_form':proprty_image_form}
        return render(request, "property/post_property.html", context_data)
    

class PropertyView(LoginRequiredMixin, View):
    login_url = "/user/login/"

    def get(self, request, *args, **kwargs):
        property_id = kwargs['pk']
        property = get_object_or_404(Property,pk=property_id)
        postal_code = property.propertyaddress.location.postal_code
        context_data = {'property':property, 'property_form':PropertyForm(instance=property),'address_form':AddressModelForm(instance=property.propertyaddress,initial={'postal_code':postal_code}),'proprty_image_form':ProprtyImageModelForm()}
        return render(request, "property/update_property.html", context_data)
    
    def post(self, request, *args, **kwargs):
        property_id = kwargs['pk']
        property = get_object_or_404(Property,pk=property_id)
        property_image = property.propertyimage_set.first()
        proprty_image_form = ProprtyImageModelForm(request.POST, request.FILES, instance=property_image)
        proprty_image_form = ProprtyImageModelForm(request.POST, request.FILES, instance=property_image)
        property_form = PropertyForm(request.POST, instance=property)
        address_form = AddressModelForm(request.POST, instance=property.propertyaddress)
        
        if 'updateImage' in request.POST:
            if proprty_image_form.is_valid():
                image_path = property_image.image.path
                if os.path.exists(image_path):
                    os.remove(image_path)
                proprty_image_form.save()
                return redirect(reverse('home'))
        else:
            if address_form.is_valid() and property_form.is_valid() :
                property_form.save()
                address_form.instance.location = address_form.cleaned_data['postal_code']
                address_form.save()
                return redirect(reverse('home'))
            else:
                print('eerroe',property_form.errors,address_form.errors)

        postal_code = property.propertyaddress.location.postal_code
        context_data = {'property':property, 'property_form':property_form,'address_form':address_form,'proprty_image_form':proprty_image_form,'message':"Update Property"}
        return render(request, "property/update_property.html", context_data)


class PropertyDetailView(LoginRequiredMixin, DetailView):

    login_url = "/user/login/"
    model = Property

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['request_property_form'] = RequestPropertyModelForm()
        return context
    
    def post(self, request, *args, **kwargs):
        request_property_form = RequestPropertyModelForm(request.POST)

        if request_property_form.is_valid():
            property = get_object_or_404(Property,pk=kwargs['pk'])
            user = get_object_or_404(UserProfile,id= request.user.id)
            request_property_form.instance.user = user
            request_property_form.instance.property = property
            request_property_form.save()
            return redirect(reverse('property_request'))


class PropertyRequestList(LoginRequiredMixin, ListView):

    login_url = "/user/login/"
    model = PropertyRequest

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.user_type == "owner":
            queryset =  self.model.objects.filter(property__owner_id=user_id, status='processing')
        else:
            queryset = self.model.objects.filter( ~Q(status = 'approved'), user_id=user_id )
        return queryset
    

class ApproveOrCancelRequest(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        property_request_id = kwargs['pk']
        reject_request = request.GET.get('reject_request',None)
        property_request = get_object_or_404(PropertyRequest,pk=property_request_id)
        if reject_request:
            if reject_request=='owner':
                property_request.status = 'rejected'
                property_request.save()
            else:
                property_request.delete()
            return redirect(reverse('home'))
        
        inital_data = {'start_date':property_request.request_start_date, 'end_date':property_request.request_end_date, 'property':property_request.property}
        approve_request_form = ApproveRequestForm(initial=inital_data)
        context = {'approve_request_form':approve_request_form}
        return render(request, "property/approve_property_request.html", context)

    def post(self, request, *args, **kwargs):
        property_request_id = kwargs['pk']
        approve_request_form = ApproveRequestForm(request.POST, request.FILES)
        if approve_request_form.is_valid():
            property_request = get_object_or_404(PropertyRequest,pk=property_request_id)
            start_date = approve_request_form.cleaned_data['start_date']
            end_date = approve_request_form.cleaned_data['end_date']
            rent_aggrement = approve_request_form.cleaned_data['rent_aggrement']
            booking = Booking.objects.create(start_date=start_date,end_date=end_date)
            property_request.booking = booking
            property_request.status = 'approved'
            property_request.save()
            Agreement.objects.create(booking=booking, document=rent_aggrement)
            return redirect(reverse('home'))
        context = {'approve_request_form':approve_request_form}
        return render(request, "property/approve_property_request.html", context)


class BookingList(LoginRequiredMixin, ListView):

    login_url = "/user/login/"
    model = Booking
    
    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.user_type == "owner":
            queryset =  self.model.objects.filter(propertyrequest__property__owner__id=user_id)
        else:    
            queryset =  self.model.objects.filter(propertyrequest__user__id=user_id)
        return queryset


class UpdateRequest( LoginRequiredMixin, UpdateView):
    model = PropertyRequest
    fields = ["request_start_date", "request_end_date"]
    template_name = 'property/update_request.html'
    success_url = '/property/request/'

    def get_form_class(self):
        form_class = super().get_form_class()
        form_class.base_fields['request_start_date'].widget = forms.widgets.DateInput(attrs={'type': 'date'})
        form_class.base_fields['request_end_date'].widget = forms.widgets.DateInput(attrs={'type': 'date'})
        return form_class

    def post(self,request, *args, **kwargs):
        if 'request_type' in request.GET:
            property_request = get_object_or_404(PropertyRequest,pk=kwargs['pk'])
            property_request.status = 'processing'
            property_request.save()

        return super(UpdateRequest, self).post(request, **kwargs)