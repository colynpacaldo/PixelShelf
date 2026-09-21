from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from apps.asset.models import Asset
from apps.shelf.models import Shelf


@login_required(login_url="login:login")
def home_view(request):
    assets = Asset.objects.filter(user=request.user)
    shelves = Shelf.objects.filter(user=request.user)

    context = {
        "asset_count": assets.count(),
        "shelf_count": shelves.count(),
        "recent_assets": assets[:6],
        "recent_shelves": shelves[:4],
    }
    return render(request, "home/home.html", context)
