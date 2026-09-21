import os

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from apps.shelf.models import Shelf, ShelfAsset
from apps.tag.models import Tag

from .forms import AssetForm
from .models import Asset


def _get_or_create_tag(name):
    tag = Tag.objects.filter(name__iexact=name).first()
    return tag or Tag.objects.create(name=name)


def _sync_tags(asset, tag_names):
    asset.tags.set([_get_or_create_tag(name) for name in tag_names])


def _report_detection(request, form):
    """Tell the user what the frame auto-detection found (if it ran)."""
    grid = getattr(form, "detected", None)
    if not grid:
        return
    frames = grid.get("cols", 1) * grid.get("rows", 1)
    if frames > 1:
        messages.info(
            request,
            f"Detected {grid['cols']}×{grid['rows']} frames "
            f"({frames} total, {grid['frame_width']}×{grid['frame_height']}px each).",
        )
    else:
        messages.warning(
            request,
            "Couldn't find separate frames in this image, so it is shown as a single "
            "frame. If frames touch each other, edit the asset and enter the frame "
            "size by hand under Advanced.",
        )


@login_required(login_url="login:login")
def asset_list_view(request):
    assets = Asset.objects.filter(user=request.user).prefetch_related("tags")

    query = request.GET.get("q", "").strip()
    if query:
        assets = assets.filter(
            Q(title__icontains=query) | Q(tags__name__icontains=query)
        ).distinct()

    tag_filter = request.GET.get("tag", "").strip()
    if tag_filter:
        assets = assets.filter(tags__name__iexact=tag_filter).distinct()

    all_tags = (
        Tag.objects.filter(assettag__asset__user=request.user)
        .distinct()
        .order_by("name")
    )

    return render(
        request,
        "asset/asset_list.html",
        {
            "assets": assets,
            "query": query,
            "tag_filter": tag_filter,
            "all_tags": all_tags,
        },
    )


@login_required(login_url="login:login")
def asset_upload_view(request):
    if request.method == "POST":
        form = AssetForm(request.POST, request.FILES)
        if form.is_valid():
            asset = form.save(commit=False)
            asset.user = request.user

            # Map spritesheet fields if provided or auto-detected
            asset.is_spritesheet = form.cleaned_data.get("is_spritesheet", False)
            if form.cleaned_data.get("frame_width"):
                asset.frame_width = form.cleaned_data["frame_width"]
            if form.cleaned_data.get("frame_height"):
                asset.frame_height = form.cleaned_data["frame_height"]

            asset.save()
            _sync_tags(asset, form.cleaned_data.get("tags", []))
            messages.success(request, "Asset uploaded.")
            _report_detection(request, form)
            return redirect("asset:detail", pk=asset.pk)
    else:
        form = AssetForm()

    return render(request, "asset/asset_form.html", {"form": form, "mode": "upload"})


@login_required(login_url="login:login")
def asset_detail_view(request, pk):
    asset = get_object_or_404(Asset, pk=pk, user=request.user)

    if request.method == "POST" and "shelf_id" in request.POST:
        shelf = get_object_or_404(Shelf, pk=request.POST.get("shelf_id"), user=request.user)
        ShelfAsset.objects.get_or_create(shelf=shelf, asset=asset)
        messages.success(request, f'Added to "{shelf.title}".')
        return redirect("asset:detail", pk=asset.pk)

    # Safe check: verifies the physical file exists without crashing if an ephemeral container restarted
    file_exists = False
    if asset.file_path:
        try:
            file_exists = asset.file_path.storage.exists(asset.file_path.name)
        except Exception:
            file_exists = False

    return render(
        request,
        "asset/asset_detail.html",
        {
            "asset": asset,
            "file_exists": file_exists,
            "user_shelves": Shelf.objects.filter(user=request.user).exclude(assets=asset),
            "shelves_containing": asset.shelves.all(),
        },
    )


@login_required(login_url="login:login")
def asset_edit_view(request, pk):
    asset = get_object_or_404(Asset, pk=pk, user=request.user)

    if request.method == "POST":
        form = AssetForm(request.POST, request.FILES, instance=asset)
        if form.is_valid():
            asset = form.save(commit=False)

            asset.is_spritesheet = form.cleaned_data.get("is_spritesheet", False)
            if form.cleaned_data.get("frame_width"):
                asset.frame_width = form.cleaned_data["frame_width"]
            if form.cleaned_data.get("frame_height"):
                asset.frame_height = form.cleaned_data["frame_height"]

            asset.save()
            _sync_tags(asset, form.cleaned_data.get("tags", []))
            messages.success(request, "Asset updated.")
            _report_detection(request, form)
            return redirect("asset:detail", pk=asset.pk)
    else:
        form = AssetForm(instance=asset)

    return render(
        request, "asset/asset_form.html", {"form": form, "mode": "edit", "asset": asset}
    )


@login_required(login_url="login:login")
def asset_delete_view(request, pk):
    asset = get_object_or_404(Asset, pk=pk, user=request.user)

    if request.method == "POST":
        asset.delete()
        messages.success(request, "Asset deleted.")
        return redirect("asset:list")

    return render(request, "asset/asset_confirm_delete.html", {"asset": asset})