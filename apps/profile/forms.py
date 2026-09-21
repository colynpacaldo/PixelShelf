from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["full_name", "bio", "profile_image"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "bio": forms.Textarea(attrs={"rows": 4, "placeholder": "Tell us about yourself"}),
        }
