import os

from django import forms
from django.core.exceptions import ValidationError

from .models import Asset

MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024  # 10MB, per the README's upload limit
ALLOWED_EXTENSIONS = {".png", ".gif"}


class AssetForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={"placeholder": "characters, tileset, ui"}),
        help_text="Comma-separated tags.",
    )

    class Meta:
        model = Asset
        fields = ["title", "file_path", "frame_width", "frame_height", "license_type", "tags"]
        labels = {"file_path": "Spritesheet (PNG or GIF, max 10MB)"}
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Hero Walk Cycle"}),
            "frame_width": forms.NumberInput(attrs={"min": 1}),
            "frame_height": forms.NumberInput(attrs={"min": 1}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # On edit, the spritesheet is optional (keep the existing file unless replaced)
        # and the free-text tag field is pre-filled from the asset's current tags.
        if self.instance.pk:
            self.fields["file_path"].required = False
            self.initial["tags"] = ", ".join(self.instance.tags.values_list("name", flat=True))

    def clean_file_path(self):
        f = self.cleaned_data.get("file_path")
        # Only newly-uploaded files carry a content_type; an unchanged
        # existing file on an edit form does not, so skip validation then.
        if f and hasattr(f, "content_type"):
            ext = os.path.splitext(f.name)[1].lower()
            if ext not in ALLOWED_EXTENSIONS:
                raise ValidationError("Only PNG and GIF files are supported.")
            if f.size > MAX_UPLOAD_SIZE_BYTES:
                raise ValidationError("File must be 10MB or smaller.")
        return f

    def clean_tags(self):
        raw = self.cleaned_data.get("tags", "")
        names = [t.strip() for t in raw.split(",") if t.strip()]
        seen, cleaned = set(), []
        for name in names:
            key = name.lower()
            if key not in seen:
                seen.add(key)
                cleaned.append(name)
        return cleaned
