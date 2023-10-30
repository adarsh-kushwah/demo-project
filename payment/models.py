from django.db import models
from property.models import Booking, UserProfile

# Create your models here.


class Bill(models.Model):
    """
    stores bills of property booking
    """

    BILL_STATUS_CHOICES = (
        ("paid", "Paid"),
        ("partial_paid", "Partially paid"),
        ("not_paid", "Not paid"),
    )
    MONTH_CHOICES = (
        ("jan", "January"),
        ("feb", "February"),
        ("mar", "March"),
        ("Apr", "April"),
        ("may", "May"),
        ("jun", "June"),
        ("jul", "July"),
        ("aug", "August"),
        ("sep", "September"),
        ("oct", "Octomber"),
        ("nov", "November"),
        ("dec", "December"),
    )
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    status = models.CharField(choices=BILL_STATUS_CHOICES, max_length=20)
    document = models.FileField(upload_to="bills", null=True)
    month = models.CharField(
        choices=MONTH_CHOICES, max_length=3, default=BILL_STATUS_CHOICES[2][0]
    )
    year = models.PositiveIntegerField(null=True)
    due_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def paid_amount(self):
        paid_amount = Payment.objects.filter(bill=self, status="success").aggregate(
            models.Sum("amount")
        )
        paid_amount = (
            paid_amount["amount__sum"] if paid_amount["amount__sum"] != None else 0
        )
        return paid_amount


class Payment(models.Model):
    """
    stores payment by renter for a booking
    """

    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    amount = models.PositiveIntegerField()
    source = models.CharField(max_length=20)
    status = models.CharField(max_length=20)
    checkout_session_id = models.CharField(max_length=100, null=True)
    payment_intent = models.CharField(max_length=100, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
