from django.contrib.auth.models import User
from django.db import models


class UserSettings(models.Model):
    TEXT_SIZE_CHOICES = (
        ("small", "Small"),
        ("medium", "Medium"),
        ("large", "Large"),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="settings")
    dark_mode = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=True)
    text_size = models.CharField(
        max_length=6,
        choices=TEXT_SIZE_CHOICES,
        default="medium",
    )

    def __str__(self):
        return f"Settings for {self.user.username}"
