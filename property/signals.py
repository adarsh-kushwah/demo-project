from property.models import Booking
from django.dispatch import receiver
from django.db.models.signals import post_save
from property.utility import send_email

@receiver(post_save, sender=Booking)
def send_mail_to_owner(sender, instance, created, **kwargs):
    if created:
        owner_email = instance.user.email
        print(owner_email)
        subject = "Booking confirmed"
        content = "Hi {} , Booking for property {} is confirmed by renter {} ."
        recipent_mail = []
        
    