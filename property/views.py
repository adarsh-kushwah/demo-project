from django.shortcuts import render, redirect
# from django.views.generic.base import TemplateView
# Create your views here.
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import get_object_or_404

from user.models import UserProfile
from property.models import Booking, PropertyImage, Property, PropertyRequest
from property.forms import PropertyForm, AddressModelForm, ProprtyImageModelForm, RequestPropertyModelForm
import os
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

class Home(View):

    def get(self, request, *args, **kwargs):
        context ={}
        if request.user.username:
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
            return redirect(reverse('home'))


class PropertyRequestList(LoginRequiredMixin, ListView):

    login_url = "/user/login/"
    model = PropertyRequest

    def get_queryset(self):
        user_id = self.request.user.id
        if self.request.user.user_type == "owner":
            queryset =  self.model.objects.filter(property__owner_id=user_id)
        else:
            queryset = self.model.objects.filter(user_id=user_id)
        return queryset