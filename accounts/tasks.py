from celery import shared_task
from django.core.mail import send_mail

@shared_task
def send_otp_email(email, otp):
    subject = 'کد تایید شما'
    message = f'کد تایید شما: {otp}'
    from_email = 'your_email@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list)
