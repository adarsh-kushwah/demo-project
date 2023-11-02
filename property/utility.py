from django.core.mail import send_mail
from django.conf import settings
import threading


def send_email(subject, mail_content, recepient_list):
    """
        function to send email
    """
    try:
        send_mail(subject, mail_content, settings.EMAIL_HOST_USER, recepient_list, fail_silently=False)
        threading.Thread (
            target=send_mail,
                kwargs={
                    "subject":"My super subject",
                    "mail_content":"My super html content",
                    "recipient_list":["to@mail.com"]
        }).start()
    except:
           pass
           

    #["adarshkushwah9165@gmail.com"]
    
		# exception = traceback.format_exc()
		# store_email_errors(subject, email_content, exception, report_email)
