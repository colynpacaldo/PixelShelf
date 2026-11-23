from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.files.storage import default_storage
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Profile


class ProfilePageTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="profile-owner",
            password="StrongPass123!",
        )
        self.client.force_login(self.user)

    def test_profile_page_renders_summary_and_custom_avatar_controls(self):
        response = self.client.get(reverse("profile:profile"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Manage your creator profile and public details.")
        self.assertContains(response, "View Public Profile")
        self.assertContains(response, "Change Photo")
        self.assertContains(response, "0 / 200")
        self.assertNotContains(response, "Currently:")
        self.assertNotContains(response, "View my public profile")

    def test_bio_is_limited_to_200_characters(self):
        response = self.client.post(
            reverse("profile:profile"),
            {
                "full_name": "",
                "bio": "a" * 201,
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Ensure this value has at most 200 characters")
        self.assertFalse(Profile.objects.get(user=self.user).bio)

    def test_remove_profile_image_clears_the_saved_image(self):
        image_buffer = BytesIO()
        Image.new("RGB", (1, 1)).save(image_buffer, format="PNG")
        upload = SimpleUploadedFile(
            "avatar.png",
            image_buffer.getvalue(),
            content_type="image/png",
        )

        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                profile = Profile.objects.create(
                    user=self.user,
                    profile_image=upload,
                )
                image_name = profile.profile_image.name

                response = self.client.post(
                    reverse("profile:profile"),
                    {
                        "full_name": "",
                        "bio": "",
                        "remove_profile_image": "on",
                    },
                )

                profile.refresh_from_db()
                self.assertRedirects(response, reverse("profile:profile"))
                self.assertFalse(profile.profile_image)
                self.assertFalse(default_storage.exists(image_name))
