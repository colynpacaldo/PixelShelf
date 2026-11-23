from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.user_settings.models import UserSettings


class UserSettingsDarkModeTests(TestCase):
    def test_new_settings_default_to_dark_mode(self):
        user = get_user_model().objects.create_user(username="default-mode")

        user_settings = UserSettings.objects.create(user=user)

        self.assertTrue(user_settings.dark_mode)

    def test_home_page_uses_dark_mode_from_user_settings(self):
        user = get_user_model().objects.create_user(username="alice", password="StrongPass123!")
        UserSettings.objects.create(user=user, dark_mode=True)

        self.client.force_login(user)
        response = self.client.get(reverse("home:home"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("dark-mode", response.content.decode())

    def test_shelves_page_uses_dark_mode_from_user_settings(self):
        user = get_user_model().objects.create_user(username="bob", password="StrongPass123!")
        UserSettings.objects.create(user=user, dark_mode=True)

        self.client.force_login(user)
        response = self.client.get(reverse("shelf:list"))

        self.assertEqual(response.status_code, 200)
        self.assertIn("dark-mode", response.content.decode())
