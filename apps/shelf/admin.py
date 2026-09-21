from django.contrib import admin

from .models import Shelf, ShelfAsset


@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "created_at")
    search_fields = ("title", "user__username")


admin.site.register(ShelfAsset)
