from django.contrib.auth.models import User
from django.db import models

from apps.asset.models import Asset


class Shelf(models.Model):
    """A user-defined collection of assets (e.g. "Boss Enemies", "UI Icons")."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shelves")
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    assets = models.ManyToManyField(Asset, through="ShelfAsset", related_name="shelves", blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class ShelfAsset(models.Model):
    """Join table backing Shelf.assets (the ERD's SHELF_ASSET table)."""

    shelf = models.ForeignKey(Shelf, on_delete=models.CASCADE)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("shelf", "asset")

    def __str__(self):
        return f"{self.shelf.title} - {self.asset.title}"
