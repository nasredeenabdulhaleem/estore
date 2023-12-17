from django.db import models

# Create your models here.
# extend the user model and make it use email login
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.conf import settings


Roles = (("User", "User"), ("Vendor", "Vendor"), ("Admin", "Admin"))


class User(AbstractUser):
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=11, blank=True, null=True)
    role = models.CharField(max_length=20, choices=Roles, default="User")

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]


# model that keeps track of verification attempts


class VerificationCount(models.Model):
    user = models.OneToOneField("User", on_delete=models.CASCADE)
    email = models.EmailField(max_length=254, unique=True)
    is_verified = models.BooleanField(default=False)
    count = models.IntegerField(default=0)
    last_attempt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name_plural = "Verification Counts"
        ordering = ["-last_attempt"]
