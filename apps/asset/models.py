import os

from django.contrib.auth.models import User
from django.db import models

from apps.tag.models import Tag

LICENSE_CHOICES = [
    ("cc0", "CC0 - Public Domain"),
    ("cc-by", "CC BY - Attribution"),
    ("cc-by-sa", "CC BY-SA - Attribution-ShareAlike"),
    ("all-rights-reserved", "All Rights Reserved"),
    ("custom", "Custom / Other"),
]


def asset_upload_path(instance, filename):
    # Namespaced by user so two creators can upload files with the same name.
    return f"assets/{instance.user_id}/{filename}"


class Asset(models.Model):
    """A single 2D game asset (typically a spritesheet) uploaded by a user."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="assets")
    title = models.CharField(max_length=255)
    file_path = models.ImageField(upload_to=asset_upload_path)
    frame_width = models.PositiveIntegerField(
        default=32, help_text="Width of a single animation frame, in pixels."
    )
    frame_height = models.PositiveIntegerField(
        default=32, help_text="Height of a single animation frame, in pixels."
    )
    license_type = models.CharField(
        max_length=50, choices=LICENSE_CHOICES, default="all-rights-reserved"
    )
    file_size_kb = models.PositiveIntegerField(default=0, editable=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, through="AssetTag", related_name="assets", blank=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Keep file_size_kb in sync whenever a new file is attached.
        if self.file_path and hasattr(self.file_path, "size"):
            try:
                self.file_size_kb = max(1, round(self.file_path.size / 1024))
            except (OSError, ValueError):
                pass
        super().save(*args, **kwargs)

    @property
    def filename(self):
        return os.path.basename(self.file_path.name) if self.file_path else ""


class AssetTag(models.Model):
    """Join table backing Asset.tags (the ERD's ASSET_TAG table)."""

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("asset", "tag")

    def __str__(self):
        return f"{self.asset.title} - {self.tag.name}"
