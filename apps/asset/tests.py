from io import BytesIO
from tempfile import TemporaryDirectory

from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse
from PIL import Image

from .models import Asset


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
        image_buffer = BytesIO()
        Image.new("RGBA", (1, 1)).save(image_buffer, format="PNG")
        upload = SimpleUploadedFile(
            "pixel.png", image_buffer.getvalue(), content_type="image/png"
        )
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
