from django.apps import AppConfig


class ShelfConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.shelf"
    label = "feature_shelf"
    verbose_name = "Shelf"
