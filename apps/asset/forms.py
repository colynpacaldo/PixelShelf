import os

from django import forms
from django.core.exceptions import ValidationError
from PIL import Image

from .models import Asset
from .spritesheet import detect_frame_grid

MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024  # 10MB, per the README's upload limit
ALLOWED_EXTENSIONS = {".png", ".gif", ".jpg", ".jpeg"}


class AssetForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter tags separated by commas (e.g. cat, hero, npc)',
            'class': 'input'
        }),
        help_text="Separate tags with commas"
    )

    class Meta:
        model = Asset
        fields = [
            'title',
            'file_path',
            'is_spritesheet',
            'license_type',
            'frame_width',
            'frame_height',
        ]
        widgets = {
            'frame_width': forms.HiddenInput(),
            'frame_height': forms.HiddenInput(),
        }
        

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            # Pre-populate the tags field with comma-separated names when editing
            self.fields['tags'].initial = ", ".join(t.name for t in self.instance.tags.all())

    def clean(self):
        """Work out the frame size for spritesheets so the user never has to.

        * Not a spritesheet  -> static sprite, no frame size at all.
        * Sizes typed by the user (or kept unchanged on an edit) -> respected.
        * Otherwise (blank sizes, or a replaced file whose old sizes no longer
          apply) -> detected from the image; see spritesheet.detect_frame_grid.
        """
        cleaned = super().clean()
        self.detected = None  # set to the detected grid so the view can tell the user

        if not cleaned.get("is_spritesheet"):
            cleaned["frame_width"] = None
            cleaned["frame_height"] = None
            return cleaned

        width, height = cleaned.get("frame_width"), cleaned.get("frame_height")
        upload = cleaned.get("file_path")
        is_new_file = bool(upload) and hasattr(upload, "content_type")
        typed_by_user = bool({"frame_width", "frame_height"} & set(self.changed_data))

        if width and height and (typed_by_user or not is_new_file):
            return cleaned  # manual override, or an unchanged edit

        try:
            if is_new_file:
                grid = detect_frame_grid(upload)
            elif self.instance.pk and self.instance.file_path:
                with self.instance.file_path.open("rb") as fh:
                    grid = detect_frame_grid(fh)
            else:
                return cleaned  # no usable file; file_path already reports its own error
        except (OSError, ValueError, Image.DecompressionBombError):
            raise ValidationError(
                "Couldn't analyse this image automatically. "
                "Please enter the frame width and height by hand."
            )

        cleaned["frame_width"] = grid["frame_width"]
        cleaned["frame_height"] = grid["frame_height"]
        self.detected = grid
        return cleaned

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
