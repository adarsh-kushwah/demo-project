from django.core.mail import send_mail
from django.conf import settings



def send_email(subject, mail_content, recepient_list):
    """
        function to send email
    """
    try:
        send_mail(subject, mail_content, settings.EMAIL_HOST_USER, recepient_list, fail_silently=False)
    except :
           print('emial esend failed')
           

    #["adarshkushwah9165@gmail.com"]
    
		# exception = traceback.format_exc()
		# store_email_errors(subject, email_content, exception, report_email)
