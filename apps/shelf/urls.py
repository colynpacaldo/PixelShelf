from django.urls import path

from .views import (
    shelf_create_view,
    shelf_delete_view,
    shelf_detail_view,
    shelf_edit_view,
    shelf_list_view,
)

app_name = "shelf"

urlpatterns = [
    path("", shelf_list_view, name="list"),
    path("new/", shelf_create_view, name="create"),
    path("<int:pk>/", shelf_detail_view, name="detail"),
    path("<int:pk>/edit/", shelf_edit_view, name="edit"),
    path("<int:pk>/delete/", shelf_delete_view, name="delete"),
]
