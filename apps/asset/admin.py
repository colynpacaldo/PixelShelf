from django.contrib import admin

from .models import Asset, AssetTag


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "title", "user", "frame_width", "frame_height",
        "license_type", "file_size_kb", "uploaded_at",
    )
    list_filter = ("license_type",)
    search_fields = ("title", "user__username")


admin.site.register(AssetTag)
