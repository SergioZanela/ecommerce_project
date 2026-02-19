"""
shop.views_auth

Authentication-related views:
- home_view: show landing page
- register_view: create user + set profile role
- login_view: authenticate user
- logout_view: end session
"""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from .forms import RegisterForm
from .permissions import _get_role


def home_view(request):
    """
    Display the application's home page.
    """
    role = _get_role(request.user) if request.user.is_authenticated else None
    return render(request, "shop/home.html", {"role": role})


def register_view(request):
    """
    Register a new user as a vendor or buyer.

    IMPORTANT:
        Profile is created automatically by signals.py,
        so here we only UPDATE the role.
    """
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            role = form.cleaned_data["role"]

            # Profile already exists because of the post_save signal
            user.profile.role = role
            user.profile.save(update_fields=["role"])

            login(request, user)
            messages.success(request, "Account created successfully.")
            return redirect("home")
    else:
        form = RegisterForm()

    return render(request, "auth/register.html", {"form": form})


def login_view(request):
    """
    Log a user in using username + password.
    """
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully.")
            return redirect("home")

        messages.error(request, "Invalid username or password.")

    return render(request, "auth/login.html")


@login_required
def logout_view(request):
    """
    Log the current user out and clear their session.
    """
    logout(request)
    messages.info(request, "Logged out.")
    return redirect("home")
