from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from user.models import UserAddress, UserProfile, Location


class AddressModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        location_list = [("", "Select state")]
        location_list.extend(
            [
                (location.state, location.state)
                for location in Location.objects.all()
                .distinct("state")
                .order_by("state")
            ]
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
        widgets = {
            "password": forms.PasswordInput(),
            "date_of_birth": forms.widgets.DateInput(attrs={"type": "date"}),
        }
    
    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        if len(str(phone_number)) != 10:
            raise ValidationError('phone number must be of 10 digits')
        return phone_number
