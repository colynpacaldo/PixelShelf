from .models import UserSettings


def user_settings(request):
    dark_mode = False
    text_size = "medium"

    if request.user.is_authenticated:
        user_settings, _ = UserSettings.objects.get_or_create(user=request.user)
        dark_mode = bool(user_settings.dark_mode)
        text_size = user_settings.text_size

    return {
        "site_dark_mode": dark_mode,
        "site_text_size": text_size,
    }
