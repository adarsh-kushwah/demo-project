from django.db import models
from user.models import UserProfile, BaseAddress
import uuid


class Property(models.Model):
    PROPERTY_TYPES_CHOICES = (
        ("apartment", "Apartment"),
        ("house", "House"),
        ("flat_1bkh", "Flat-1bhk"),
        ("flat_2bkh", "Flat-2bhk"),
        ("flat_3bkh", "Flat-3bhk"),
    )
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=True)
    property_type = models.CharField(
        max_length=20, choices=PROPERTY_TYPES_CHOICES, default="house"
    )
    is_available = models.BooleanField(default=True)
    availability_date = models.DateField(blank=True, null=True)
    rent_amount = models.PositiveIntegerField()
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.name} {self.property_type}"


class PropertyAddress(BaseAddress):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)


class PropertyImage(models.Model):
    """
    model to store images of property
    """

    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="property_images")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Amenity(models.Model):
    """
    stores amenity of property
    """

    STATUS_CHOICES = (
        ("available", "Available"),
        ("unavailable", "Unavailable"),
        ("maintenance", "Under Maintenance"),
    )
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="available"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PropertyRequestResponse(models.Model):
    """
    stores renter's request to property and owner's response to property
    here user is person who requests or response

    request Token of request sent by renter and response by owner on renter's request
    will be Same
    """

    STATUS_CHOICES = (
        ("processing", "Processing"),
        ("responsed", "Responsed"),
        ("rejected", "Rejected"),
        ("approved", "Approved"),
        ("left", "Lefted"),
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="processing"
    )
    request_token = models.CharField(default=uuid.uuid4, max_length=36)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    request_response_property = models.ForeignKey(
        Property, on_delete=models.SET_NULL, null=True
    )
    rent_amount = models.PositiveIntegerField(null=True)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = (
            "request_token",
            "user",
            "request_response_property",
            "created_at",
        )

    @property
    def renter(self):
        return PropertyRequestResponse.objects.get(
            user__user_type="renter", request_token=self.request_token
        ).user


class Booking(models.Model):
    """
    stores Property booking by renter
    """

    property_request_response = models.OneToOneField(
        PropertyRequestResponse, on_delete=models.CASCADE, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def renter(self):
        request_token = self.property_request_response.request_token
        property_request_response = PropertyRequestResponse.objects.get(
            request_token=request_token, user__user_type="renter"
        )
        return property_request_response.user


class Agreement(models.Model):
    """
    stores agreement between owner and renter
    """

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    document = models.FileField(upload_to="aggrement/renter")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
