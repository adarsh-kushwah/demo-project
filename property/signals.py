from property.models import Booking
from django.dispatch import receiver
from django.db.models.signals import post_save
from property.utility import send_email
import threading


@receiver(post_save, sender=Booking)
def send_mail_to_owner(sender, instance, created, **kwargs):
    if created:
        recepient_email = [instance.property_request_response.user.email]
        subject = "Booking confirmed"
        content = f"Hi {instance.property_request_response.user.get_full_name()} , Booking for property {instance.property_request_response.request_response_property.name} is confirmed by renter {instance.renter.get_full_name()} ."

        threading.Thread(
            target=send_email,
            kwargs={
                "subject": subject,
                "mail_content": content,
                "recepient_list": recepient_email,
            },
        ).start()
