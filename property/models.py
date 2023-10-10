from django.db import models
from user.models import UserProfile, BaseAddress


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
        return f'{self.name} {self.property_type}'


class PropertyAddress(BaseAddress):
    property = models.OneToOneField(Property, on_delete=models.CASCADE)

    def full_address(self):
        return f"{self.street_address}, {self.location.city}, {self.location.postal_code}, {self.location.state}"


class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="property_images")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Amenity(models.Model):
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



class PropertyRequest(models.Model):
    STATUS_CHOICES = (
        ("processing", "Processing"),
        ("rejected", "Rejected"),
        ("approved", "Approved"),
    )
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    property = models.ForeignKey(Property, on_delete=models.SET_NULL, null=True)
    booking = models.OneToOneField('Booking', on_delete=models.SET_NULL, null=True)
    request_start_date = models.DateField()
    request_end_date = models.DateField(blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="processing"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Booking(models.Model):
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Agreement(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    document = models.FileField(upload_to="aggrement")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Bill(models.Model):
    BILL_STATUS_CHOICES = (
        ("paid", "Paid"),
        ("partial_paid", "Partially paid"),
        ("not_paid", "Not paid"),
    )
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=BILL_STATUS_CHOICES)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)


class Payment(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField()
    source = models.CharField(max_length=20)
    status = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)