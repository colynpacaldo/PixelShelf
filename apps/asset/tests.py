from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from apps.shelf.models import Shelf

from .models import Asset


def make_test_image():
    image_buffer = BytesIO()
    Image.new("RGBA", (1, 1)).save(image_buffer, format="PNG")
    return SimpleUploadedFile(
        "pixel.png", image_buffer.getvalue(), content_type="image/png"
    )


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class AssetUploadTests(TestCase):
    def test_upload_defaults_frame_offsets_to_zero(self):
        upload = make_test_image()
        user = get_user_model().objects.create_user(
            username="asset-uploader", password="StrongPass123!"
        )
        self.client.force_login(user)

        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                response = self.client.post(
                    reverse("asset:upload"),
                    {
                        "title": "Pixel",
                        "file_path": upload,
                        "license_type": "all-rights-reserved",
                    },
                )

        self.assertEqual(response.status_code, 302)
        asset = Asset.objects.get(user=user, title="Pixel")
        self.assertEqual(asset.frame_offset_x, 0)
        self.assertEqual(asset.frame_offset_y, 0)


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
        },
    }
)
class AssetAccessTests(TestCase):
    def create_asset(self, owner):
        return Asset.objects.create(
            user=owner,
            title="Pixel",
            file_path=make_test_image(),
            license_type="all-rights-reserved",
        )

    def test_owner_can_download_asset(self):
        owner = get_user_model().objects.create_user(username="owner")

        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                asset = self.create_asset(owner)
                self.client.force_login(owner)

                response = self.client.get(reverse("asset:download", args=[asset.pk]))

                self.assertEqual(response.status_code, 200)
                self.assertIn("attachment", response["Content-Disposition"])
                response.close()

    def test_public_shelf_asset_is_clickable_and_downloadable(self):
        owner = get_user_model().objects.create_user(username="owner")
        viewer = get_user_model().objects.create_user(username="viewer")
        shelf = Shelf.objects.create(user=owner, title="Public shelf", is_public=True)

        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                asset = self.create_asset(owner)
                shelf.assets.add(asset)
                self.client.force_login(viewer)

                shelf_response = self.client.get(
                    reverse("shelf:detail", args=[shelf.pk])
                )
                self.assertContains(
                    shelf_response, reverse("asset:detail", args=[asset.pk])
                )

                detail_response = self.client.get(
                    reverse("asset:detail", args=[asset.pk])
                )
                self.assertContains(detail_response, "Download")
                self.assertContains(detail_response, "All Rights Reserved")

                download_response = self.client.get(
                    reverse("asset:download", args=[asset.pk])
                )
                self.assertEqual(download_response.status_code, 200)
                self.assertIn("attachment", download_response["Content-Disposition"])
                download_response.close()

    def test_private_asset_is_not_accessible_to_other_users(self):
        owner = get_user_model().objects.create_user(username="owner")
        viewer = get_user_model().objects.create_user(username="viewer")

        with TemporaryDirectory() as media_root:
            with override_settings(MEDIA_ROOT=media_root):
                asset = self.create_asset(owner)
                self.client.force_login(viewer)

                self.assertEqual(
                    self.client.get(reverse("asset:detail", args=[asset.pk])).status_code,
                    404,
                )
                self.assertEqual(
                    self.client.get(reverse("asset:download", args=[asset.pk])).status_code,
                    404,
                )
