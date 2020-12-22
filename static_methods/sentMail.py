import smtplib

from django.core.mail import send_mail, BadHeaderError
from traffic_app_final.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, EMAIL_PORT, EMAIL_VERIFICATION_TITLE, \
    SSL_CONTEXT, EMAIL_HOST


def send_verificationPIN_bymail(to_email, PIN):
    try:
        send_mail(
            f'{EMAIL_VERIFICATION_TITLE} - Verification',
            f'Welcome to {EMAIL_VERIFICATION_TITLE},\r\r\n'
            f'Your Email to login: {to_email},\r\r\n'
            f'Your PIN code for verification: {PIN}\r\r\n',
            EMAIL_HOST_USER,
            [to_email],
            fail_silently=False,
        )
    except Exception as e:
        return False
    return True


def send_resetpassword_bymail(to_email, PIN):
    try:
        send_mail(
            f'{EMAIL_VERIFICATION_TITLE} - Reset Password',
            f'Someone request a rest password for your account.\nReset password PIN is : \b{PIN}',
            EMAIL_HOST_USER,
            [to_email],
            fail_silently=False,
        )
    except Exception as e:
        return False
    return True
