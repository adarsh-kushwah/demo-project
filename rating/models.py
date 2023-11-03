from django.db import models
from user.models import UserProfile
from property.models import Property, Booking


class AbstractPropertyRatingReview(models.Model):
    renter = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class PropertyRating(AbstractPropertyRatingReview):
    """
    store rating of Property given by renter
    """

    booking = models.OneToOneField(Booking, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveIntegerField(default=0)


class RenterRating(AbstractPropertyRatingReview):
    """
    store rating of Renter given by property owner
    """

    owner = models.ForeignKey(
        UserProfile, related_name="rating_to", on_delete=models.SET_NULL, null=True
    )
    booking = models.OneToOneField(Booking, on_delete=models.SET_NULL, null=True)
    rating = models.PositiveIntegerField(default=0)


class PropertyReview(AbstractPropertyRatingReview):
    """
    store review of Property given by renter
    """

    booking = models.OneToOneField(Booking, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=50)


class RenterReview(AbstractPropertyRatingReview):
    """
    store review of Renter given by property owner
    """

    owner = models.ForeignKey(
        UserProfile, related_name="review_to", on_delete=models.SET_NULL, null=True
    )
    booking = models.OneToOneField(Booking, on_delete=models.SET_NULL, null=True)
    description = models.CharField(max_length=50)
