from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.user_settings.models import UserSettings


class RegistrationDefaultSettingsTests(TestCase):
    def test_new_account_defaults_to_dark_mode(self):
        response = self.client.post(
            reverse("register:register"),
            {
                "username": "new-user",
                "password": "StrongPass123!",
                "confirm_password": "StrongPass123!",
            },
        )

        self.assertRedirects(response, reverse("login:login"))
        user = get_user_model().objects.get(username="new-user")
        self.assertTrue(UserSettings.objects.get(user=user).dark_mode)
