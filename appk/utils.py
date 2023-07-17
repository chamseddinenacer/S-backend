from django.core.mail import send_mail
from django.conf import settings

def send_leave_request_email():
    subject = 'Leave chamsaaa'
    message = f'Dear your leave request has been submitted successfully.'
    from_email = settings.EMAIL_HOST_USER
    recipient_list = ["chamseddine.nacer@isimg.tn"]
    
    send_mail(subject, message, from_email, recipient_list)
