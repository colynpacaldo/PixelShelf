from django.apps import AppConfig


class ProfileConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.profile"
    label = "feature_profile"
    verbose_name = "Profile"
