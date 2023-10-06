from django import forms
from django.core.exceptions import ValidationError

from user.models import Location
from property.models import Property, PropertyAddress, PropertyImage, PropertyRequest


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ["address"]
        widgets = {"owner": forms.HiddenInput(),"availability_date":forms.widgets.DateInput(attrs={'type': 'date'})}


class ProprtyImageModelForm(forms.ModelForm):
    class Meta:
        model = PropertyImage
        fields = ['image']
        # widgets = {"image":}

class AddressModelForm(forms.ModelForm):
    postal_code = forms.CharField()
    class Meta:
        model = PropertyAddress
        fields = ["postal_code", "street_address"]
    
    def clean_postal_code(self):
        postal_code = self.cleaned_data['postal_code']
        location = Location.objects.filter(postal_code=postal_code)
        
        if location.exists():
            return location.first()
        else:
            raise ValidationError("Pincode does not exists.")


class RequestPropertyModelForm(forms.ModelForm):
    
    class Meta:
        model = PropertyRequest
        fields = ["request_start_date", "request_end_date"]
        widgets = {"request_start_date":forms.widgets.DateInput(attrs={'type': 'date'}),"request_end_date":forms.widgets.DateInput(attrs={'type': 'date'})}