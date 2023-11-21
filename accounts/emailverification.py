# Email verification and activation class

from django.conf import settings
import json
from datetime import datetime, timedelta, timezone
from accounts.models import User

import jwt
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string

# from jwt.utils import get_int_from_datetime


class EmailVerification:
    def __init__(self):
        self.DOMAIN = settings.DOMAIN_NAME
        self.SECRET_KEY = settings.SECRET_KEY

    def generate_token(self, email):
        """
        Encode the message to JWT(JWS).
        """
        # instance = JWT()

        # Create a JWK object from the SECRET_KEY
        # jwk = JWK()
        # jwk.load_key(self.SECRET_KEY)

        message = {
            "iss": self.DOMAIN,
            "email": email,
            "iat": datetime.now(timezone.utc).timestamp(),
            "exp": (datetime.now(timezone.utc) + timedelta(hours=1)).timestamp(),
        }
        print("i got before teken encode")
        print(type(self.SECRET_KEY))
        token = jwt.encode(message, self.SECRET_KEY, algorithm="HS256")

        print("TOKEN:", token)
        return token

    def decode_token(self, token):
        """
        Decode the message from JWT(JWS).
        """

        token = jwt.decode(token, self.SECRET_KEY, algorithms="HS256",verify=True)

        print("Decoded TOKEN:", token)
        return token

    def activate_user(self, email):
        """
        Activates user
        returns True if user was successfully activated and False otherwise
        """
        try:
            user = User.objects.get(email=email)
        except user.DoesNotExist:
            return False
        user.is_active = True
        user.save()
        return user.is_active

    def resend_verification(self, user, email):
        token = self.generate_token(email)
        self.send_email(user, token)

    def send_email(self, user, token):
        """
        Sends email to user
        """
        verification_link = (
            f"http://{self.DOMAIN}/accounts/verify-email/{token}"
        )
        print(f"sending to {user.email}")
        context = {
            "name": user.username,
            "subject": "Email Verification",
            "verification_link": verification_link,
        }
        subject = "Email Verification"
        email_content = render_to_string("emails/verification-email.html", context)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]
        message = EmailMessage(subject, email_content, email_from, recipient_list)
        message.content_subtype = "html"
        # try:
            # Send the email
        print("i got before sendining mail")
        # print(send_mail(subject=subject,from_email=email_from,recipient_list=recipient_list,html_message=email_content,message="email_content"))
        message.send()
        print("i sent")
        return True
        # except Exception as e:

        #     print("i failed")
        #     print(e)
        #     return False

    def send_verification_email(self, user):
        token = self.generate_token(user.email)
        self.send_email(user, token)
        return True
