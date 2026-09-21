from django.contrib import admin

from .models import Asset, AssetTag


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = (
        "title", "user", "is_spritesheet", "frame_width", "frame_height",
        "license_type", "file_size_kb", "uploaded_at",
    )
    list_filter = ("is_spritesheet", "license_type")
    search_fields = ("title", "user__username")


admin.site.register(AssetTag)
