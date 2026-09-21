from django.urls import path

from .views import (
    asset_delete_view,
    asset_detail_view,
    asset_edit_view,
    asset_list_view,
    asset_upload_view,
)

app_name = "asset"

urlpatterns = [
    path("", asset_list_view, name="list"),
    path("upload/", asset_upload_view, name="upload"),
    path("<int:pk>/", asset_detail_view, name="detail"),
    path("<int:pk>/edit/", asset_edit_view, name="edit"),
    path("<int:pk>/delete/", asset_delete_view, name="delete"),
]
