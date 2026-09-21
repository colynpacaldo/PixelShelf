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
    is_spritesheet = models.BooleanField(
        default=False,
        help_text="Tick if this image is a sheet of animation frames rather than a single sprite.",
    )
    # Only meaningful for spritesheets. Detected automatically on upload
    # (see spritesheet.py); the user can still override them by hand.
    frame_width = models.PositiveIntegerField(
        null=True, blank=True, help_text="Width of a single animation frame, in pixels."
    )
    frame_height = models.PositiveIntegerField(
        null=True, blank=True, help_text="Height of a single animation frame, in pixels."
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

    @property
    def is_animated(self):
        """True when this is a spritesheet with a usable frame size."""
        return bool(self.is_spritesheet and self.frame_width and self.frame_height)

    @property
    def frame_count(self):
        """How many frames the animator will cut out of the sheet (1 if static)."""
        if not self.is_animated:
            return 1
        try:
            cols = max(1, self.file_path.width // self.frame_width)
            rows = max(1, self.file_path.height // self.frame_height)
        except (OSError, ValueError):
            return 1
        return cols * rows

    @property
    def size_label(self):
        """Short human label for cards: frame size for sheets, image size otherwise."""
        try:
            if self.is_animated:
                label = f"{self.frame_width}×{self.frame_height}px"
                frames = self.frame_count
                return f"{label} · {frames} frames" if frames > 1 else label
            return f"{self.file_path.width}×{self.file_path.height}px"
        except (OSError, ValueError):
            return ""


class AssetTag(models.Model):
    """Join table backing Asset.tags (the ERD's ASSET_TAG table)."""

    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("asset", "tag")

    def __str__(self):
        return f"{self.asset.title} - {self.tag.name}"
