from django.db import models
from user.models import UserProfile
from property.models import Property
# Create your models here.

class PropertyRating(models.Model):
    """
    store rating of Property given by renter
    """

    rating_by = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RenterRating(PropertyRating):
    """
    store rating of Renter given by property owner
    """

    rating_to = models.ForeignKey(
        UserProfile, related_name="rating_to", on_delete=models.SET_NULL, null=True
    )


class PropertyReview(models.Model):
    """
    store review of Property given by renter
    """

    review_by = models.ForeignKey(
        UserProfile, on_delete=models.SET_NULL, null=True, blank=True
    )
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class RenterReview(PropertyReview):
    """
    store review of Renter given by property owner
    """

    review_to = models.ForeignKey(
        UserProfile, related_name="review_to", on_delete=models.SET_NULL, null=True
    )