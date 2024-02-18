from django.db import models
from django.conf import settings
from django.utils import timezone


class ChatUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="chat_user"
    )
    chat_id = models.CharField(max_length=255, unique=True)
    role = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
