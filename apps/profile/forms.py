from django import forms

from .models import Profile


class ProfileForm(forms.ModelForm):
    bio = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.Textarea(
            attrs={
                "rows": 4,
                "maxlength": 200,
                "placeholder": "Tell us about yourself",
            }
        ),
    )

    class Meta:
        model = Profile
        fields = ["full_name", "bio", "profile_image"]
        widgets = {
            "full_name": forms.TextInput(attrs={"placeholder": "Your full name"}),
            "profile_image": forms.FileInput(
                attrs={"class": "avatar-upload-input", "accept": "image/*"}
            ),
        }
