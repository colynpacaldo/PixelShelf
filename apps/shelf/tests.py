from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from apps.asset.models import Asset

from .models import Shelf


def make_test_image(filename):
    image_buffer = BytesIO()
    Image.new("RGBA", (1, 1)).save(image_buffer, format="PNG")
    return SimpleUploadedFile(
        filename, image_buffer.getvalue(), content_type="image/png"
    )


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class CommunityQueryTests(TestCase):
    def setUp(self):
        media_directory = TemporaryDirectory()
        self.addCleanup(media_directory.cleanup)
        media_settings = override_settings(MEDIA_ROOT=media_directory.name)
        media_settings.enable()
        self.addCleanup(media_settings.disable)

        user_model = get_user_model()
        self.owner = user_model.objects.create_user(username="asset-owner")
        viewer = user_model.objects.create_user(username="community-viewer")

        self.public_shelf = Shelf.objects.create(
            user=self.owner, title="Public Collection", is_public=True
        )
        private_shelf = Shelf.objects.create(
            user=self.owner, title="Private Collection", is_public=False
        )
        self.public_asset = Asset.objects.create(
            user=self.owner,
            title="Shared Pixel",
            file_path=make_test_image("shared.png"),
            license_type="cc0",
        )
        self.private_asset = Asset.objects.create(
            user=self.owner,
            title="Private Pixel",
            file_path=make_test_image("private.png"),
            license_type="all-rights-reserved",
        )
        self.public_shelf.assets.add(self.public_asset)
        private_shelf.assets.add(self.private_asset)
        self.client.force_login(viewer)

    def test_community_page_joins_public_shelf_with_owner(self):
        response = self.client.get(reverse("shelf:community"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Public Collection")
        self.assertContains(response, "asset-owner")
        self.assertNotContains(response, "Private Collection")
        self.assertIn("JOIN", response.context["generated_sql"].upper())
        self.assertContains(
            response, reverse("shelf:community_assets")
        )

    def test_community_assets_subquery_includes_only_assets_on_public_shelves(self):
        response = self.client.get(reverse("shelf:community_assets"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Shared Pixel")
        self.assertContains(response, "asset-owner")
        self.assertNotContains(response, "Private Pixel")
        generated_sql = response.context["generated_sql"].upper()
        self.assertIn(" IN (", generated_sql)
        self.assertIn("SELECT", generated_sql)