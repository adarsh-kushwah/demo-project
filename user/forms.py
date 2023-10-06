from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from user.models import UserAddress, UserProfile, Location


class AddressModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        location_list = [("", "Select state")]
        location_list.extend(
            [(location.state, location.state) for location in Location.objects.all()]
        )
        self.fields["state"].choices = location_list

    state = forms.ChoiceField(
        choices=[], widget=forms.Select(attrs={"id": "SelectStateDropDown"})
    )
    city = forms.CharField(widget=forms.Select(attrs={"id": "SelectCityDropDown"}))
    postal_code = forms.CharField(
        widget=forms.Select(attrs={"id": "SelectPostalCodeDropDown"})
    )

    class Meta:
        model = UserAddress
        fields = ["state", "city", "postal_code", "street_address"]


class UserProfileModelForm(UserCreationForm):
    class Meta:
        model = UserProfile
        fields = [
            "username",
            "first_name",
            "last_name",
            "user_type",
            "date_of_birth",
            "gender",
            "marital_status",
            "profile_picture",
            "phone_number",
            "alternate_phone_number",
        ]
        widgets = {"password": forms.PasswordInput()}
