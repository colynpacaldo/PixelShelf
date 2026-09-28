from django import forms

from .models import Shelf


class ShelfForm(forms.ModelForm):
    class Meta:
        model = Shelf
        fields = ["title", "description", "is_public"]
        labels = {"is_public": "Make this shelf public"}
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Boss Enemies"}),
            "description": forms.Textarea(attrs={"rows": 3, "placeholder": "What's this shelf for? (optional)"}),
        }
