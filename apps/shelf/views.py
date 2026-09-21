from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ShelfForm
from .models import Shelf, ShelfAsset


@login_required(login_url="login:login")
def shelf_list_view(request):
    shelves = Shelf.objects.filter(user=request.user).prefetch_related("assets")
    return render(request, "shelf/shelf_list.html", {"shelves": shelves})


@login_required(login_url="login:login")
def shelf_create_view(request):
    if request.method == "POST":
        form = ShelfForm(request.POST)
        if form.is_valid():
            shelf = form.save(commit=False)
            shelf.user = request.user
            shelf.save()
            messages.success(request, "Shelf created.")
            return redirect("shelf:detail", pk=shelf.pk)
    else:
        form = ShelfForm()

    return render(request, "shelf/shelf_form.html", {"form": form, "mode": "create"})


@login_required(login_url="login:login")
def shelf_detail_view(request, pk):
    shelf = get_object_or_404(Shelf, pk=pk, user=request.user)

    if request.method == "POST" and "remove_asset_id" in request.POST:
        ShelfAsset.objects.filter(shelf=shelf, asset_id=request.POST.get("remove_asset_id")).delete()
        messages.success(request, "Removed from shelf.")
        return redirect("shelf:detail", pk=shelf.pk)

    return render(
        request,
        "shelf/shelf_detail.html",
        {"shelf": shelf, "assets": shelf.assets.all()},
    )


@login_required(login_url="login:login")
def shelf_edit_view(request, pk):
    shelf = get_object_or_404(Shelf, pk=pk, user=request.user)

    if request.method == "POST":
        form = ShelfForm(request.POST, instance=shelf)
        if form.is_valid():
            form.save()
            messages.success(request, "Shelf updated.")
            return redirect("shelf:detail", pk=shelf.pk)
    else:
        form = ShelfForm(instance=shelf)

    return render(
        request, "shelf/shelf_form.html", {"form": form, "mode": "edit", "shelf": shelf}
    )


@login_required(login_url="login:login")
def shelf_delete_view(request, pk):
    shelf = get_object_or_404(Shelf, pk=pk, user=request.user)

    if request.method == "POST":
        shelf.delete()
        messages.success(request, "Shelf deleted.")
        return redirect("shelf:list")

    return render(request, "shelf/shelf_confirm_delete.html", {"shelf": shelf})
