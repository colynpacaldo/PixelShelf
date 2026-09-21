from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect


def login_view(request):
    """Authenticate an existing user. Owned entirely by the Login feature."""
    if request.user.is_authenticated:
        return redirect("home:home")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home:home")

        return render(request, "login/login.html", {
            "error": "Invalid username or password.",
            "username": username,
        })

    return render(request, "login/login.html")


@login_required(login_url="login:login")
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect("login:login")
