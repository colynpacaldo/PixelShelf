from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

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
