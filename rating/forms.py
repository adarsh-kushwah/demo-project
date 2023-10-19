from django import forms
from rating.models import PropertyReview, RenterReview


class PropertyReviewModelForm(forms.ModelForm):
    class Meta:
        model = PropertyReview
        fields = ["description"]


class RenterReviewModelForm(forms.ModelForm):
    class Meta:
        model = RenterReview
        fields = ["description"]