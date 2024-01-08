import os
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from accounts.models import User, VerificationCount
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone


class EmailVerification:
    """
    A class used to handle email verification and activation.
    """

    def __init__(self):
        self.domain = settings.DOMAIN_NAME
        self.secret_key = os.environ.JWT_SECRET

    def generate_token(self, email):
        """
        Generates a JWT token for the given email.

        Args:
            email (str): The email for which the token will be generated.

        Returns:
            str: The generated JWT token.
        """
        payload = {
            "iss": self.domain,
            "email": email,
            "iat": datetime.now(timezone.utc).timestamp(),
            "exp": (datetime.now(timezone.utc) + timedelta(hours=1)).timestamp(),
        }
        token = jwt.encode(payload, self.secret_key, algorithm="HS256")
        return token

    def decode_token(self, token):
        """
        Decodes the given JWT token.

        Args:
            token (str): The JWT token to be decoded.

        Returns:
            dict or bool: The decoded token as a dictionary if valid, False otherwise.
        """
        try:
            decoded_token = jwt.decode(
                token, self.secret_key, algorithms="HS256", verify=True
            )
            print(decoded_token)
            return decoded_token
        except InvalidTokenError as e:
            print(e)
            return False

    def activate_user(self, email):
        """
        Activates the user with the given email.

        Args:
            email (str): The email of the user to be activated.

        Returns:
            bool: True if the user was successfully activated, False otherwise.
        """
        try:
            user = User.objects.get(email=email)
            verification = VerificationCount.objects.get(user=user)
            verification.is_verified = True
            verification.save()
            return True
        except User.DoesNotExist:
            return False

    def send_verification_email(self, user):
        """
        Generates a token and sends a verification email to the user.

        Args:
            user (User): The user object to whom the verification email will be sent.

        Returns:
            bool: True if the email was successfully sent, False otherwise.
        """
        token = self.generate_token(user.email)
        if not token:
            return False

        verification_link = f"http://{self.domain}/accounts/verify-email/{token}/"
        context = {
            "name": user.username,
            "subject": "Email Verification",
            "verification_link": verification_link,
        }

        subject = "Email Verification"
        email_content = render_to_string("emails/verification-email.html", context)
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        try:
            send_mail(
                subject=subject,
                message="",
                from_email=email_from,
                recipient_list=recipient_list,
                html_message=email_content,
            )
            return True
        
        except Exception as e:
            return False

    def resend_verification(self, user, email):
        """
        Resends the verification email to the specified user.

        Args:
            user (User): The user object to whom the verification email will be sent.
            email (str): The email address to which the verification email will be sent.

        Returns:
            None
        """
        # token = self.generate_token(email)
        self.send_verification_email(user)
