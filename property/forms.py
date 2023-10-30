from django import forms
from django.core.exceptions import ValidationError

from user.models import Location
from property.models import (
    Property,
    PropertyAddress,
    PropertyImage,
    Agreement,
    PropertyRequestResponse,
    Amenity
)


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ["address"]
        widgets = {
            "owner": forms.HiddenInput(),
            "availability_date": forms.widgets.DateInput(attrs={"type": "date"}),
        }


class ProprtyImageModelForm(forms.ModelForm):

    class Meta:
        model = PropertyImage
        fields = ["image"]


class AddressModelForm(forms.ModelForm):
    postal_code = forms.CharField()

    class Meta:
        model = PropertyAddress
        fields = ["postal_code", "street_address"]

    def clean_postal_code(self):
        postal_code = self.cleaned_data["postal_code"]
        location = Location.objects.filter(postal_code=postal_code)

        if location.exists():
            return location.first()
        else:
            raise ValidationError("Pincode does not exists.")


class AmenityModelForm(forms.ModelForm):
    
    class Meta:
        model = Amenity
        fields = ["name", "status"]


class RequestPropertyModelForm(forms.ModelForm):
    class Meta:
        model = PropertyRequestResponse
        fields = ["start_date", "end_date", "rent_amount"]
        widgets = {
            "start_date": forms.widgets.DateInput(attrs={"type": "date"}),
            "end_date": forms.widgets.DateInput(attrs={"type": "date"}),
        }


class PropertyRequestResponseForm(forms.ModelForm):
    class Meta:
        model = PropertyRequestResponse
        exclude = ["user", "property", "status", "request_response_property"]
        labels = {"rent_amount": "Requested rent amount", "document": "sent aggrement"}
        widgets = {
            "start_date": forms.widgets.DateInput(attrs={"type": "date"}),
            "end_date": forms.widgets.DateInput(attrs={"type": "date"}),
            "request_token": forms.HiddenInput(),
        }


class AgreementModelForm(forms.ModelForm):
    class Meta:
        model = Agreement
        fields = ["document"]
        labels = {"document": "sent aggrement"}
        help_texts = {
            "document": "Upload agreement after doing signature on agreement send by owner",
        }
