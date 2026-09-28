from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render

from apps.shelf.models import Shelf

from .forms import ProfileForm
from .models import Profile


@login_required(login_url="login:login")
def profile_view(request):
    profile, _created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("profile:profile")
    else:
        form = ProfileForm(instance=profile)

    return render(request, "profile/profile.html", {"form": form, "profile": profile})


@login_required(login_url="login:login")
def public_profile_view(request, username):
    owner = get_object_or_404(User, username=username)
    profile = Profile.objects.filter(user=owner).first()
    shelves = Shelf.objects.filter(user=owner, is_public=True).prefetch_related("assets")
    return render(
        request,
        "profile/public_profile.html",
        {"owner": owner, "profile": profile, "shelves": shelves},
    )
