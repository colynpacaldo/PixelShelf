from django.db import models


class Tag(models.Model):
    """A short, reusable label creators can attach to their assets
    (e.g. "character", "tileset", "ui", "boss")."""

    name = models.CharField(max_length=50, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name
