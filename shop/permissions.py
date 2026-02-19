"""
shop.permissions

Provides decorators and helper functions to restrict access based on:
- login status
- user role (vendor or buyer)
"""

from functools import wraps
from django.contrib import messages
from django.shortcuts import redirect
from .models import Profile


def _get_role(user) -> str | None:
    """
    Safely fetch a user's role from their Profile.

    Args:
        user: Django user instance.

    Returns:
        Role string ('vendor' or 'buyer') if profile exists; otherwise None.
    """
    if not getattr(user, "is_authenticated", False):
        return None

    try:
        return user.profile.role
    except (Profile.DoesNotExist, AttributeError):
        return None


def vendor_required(view_func):
    """
    Decorator that restricts access to vendor users only.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        if _get_role(request.user) != Profile.ROLE_VENDOR:
            msg = "You must be a vendor to access that page."
            messages.error(request, msg)
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper


def buyer_required(view_func):
    """
    Decorator that restricts access to buyer users only.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect("login")

        if _get_role(request.user) != Profile.ROLE_BUYER:
            msg = "You must be a buyer to access that page."
            messages.error(request, msg)
            return redirect("home")

        return view_func(request, *args, **kwargs)

    return wrapper
