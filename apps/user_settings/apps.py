from django.apps import AppConfig


class UserSettingsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.user_settings"
    label = "feature_user_settings"
    verbose_name = "User Settings"
