from django import forms

from .models import UserSettings


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = ["dark_mode", "text_size", "email_notifications"]
        widgets = {
            "text_size": forms.RadioSelect,
        }
