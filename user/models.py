from django.db import models
from django.contrib.auth.models import AbstractUser


class Location(models.Model):
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.postal_code},{self.city},{self.state}"


class UserProfile(AbstractUser):
    USER_TYPE_CHOICES = (("renter", "Renter"), ("owner", "Owner"))
    MARRIAGE_STATUS_CHOICES = (
        ("single", "Single"),
        ("married", "Married"),
        ("divorced", "Divorced"),
        ("widowed", "Widowed"),
        ("other", "Other"),
    )
    GENDER_CHOICE = (
        ("male", "Male"),
        ("female", "Female"),
        ("other", "Other"),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICE)
    marital_status = models.CharField(
        max_length=20, choices=MARRIAGE_STATUS_CHOICES, default="single"
    )
    profile_picture = models.ImageField(
        upload_to="profile_picture", blank=True, null=True
    )
    phone_number = models.CharField(max_length=15)
    alternate_phone_number = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username


class BaseAddress(models.Model):
    street_address = models.CharField(max_length=255)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True

    def full_address(self):
        if self.location:
            return f"{self.street_address}, {self.location.city }, {self.location.postal_code}, {self.location.state}"
        return f"{self.street_address}"


class UserAddress(BaseAddress):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.street_address
