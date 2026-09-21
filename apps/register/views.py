from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.shortcuts import render, redirect


def register_view(request):
    """Create a new user account. Owned entirely by the Register feature."""
    if request.user.is_authenticated:
        return redirect("home:home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        error = None
        if not username or not password:
            error = "Username and password are required."
        elif password != confirm_password:
            error = "Passwords do not match."
        elif User.objects.filter(username=username).exists():
            error = "Username already exists."

        if error:
            return render(request, "register/register.html", {
                "error": error,
                "username": username,
            })

        # The .exists() check above can race with a near-simultaneous
        # duplicate submission (double-click, resubmitted form, etc.).
        # Catch the database's own uniqueness error as a safety net so the
        # user sees a friendly message instead of a server error.
        try:
            with transaction.atomic():
                User.objects.create_user(username=username, password=password)
        except IntegrityError:
            return render(request, "register/register.html", {
                "error": "Username already exists.",
                "username": username,
            })

        messages.success(request, "Account created. You can now log in.")
        return redirect("login:login")

    return render(request, "register/register.html")
