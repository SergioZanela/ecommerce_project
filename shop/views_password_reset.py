"""
shop.views_password_reset

Password reset flow with expiring tokens:
- password_forgot_view: user enters email -> send reset link
- password_reset_view: validate token -> set new password
"""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone

from .models import PasswordResetToken

User = get_user_model()


def password_forgot_view(request):
    """
    User submits email. If exists, create token and email reset link.
    """
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()

        # Look up user by email (case-insensitive).
        # If not found, user will be None.
        user = User.objects.filter(email__iexact=email).first()

        # Always show same message to prevent email enumeration
        messages.info(
            request,
            "If that email exists, a reset link has been sent."
        )

        if user:
            # ✅ FIX: generate token properly (token field is required + unique)
            token_obj = PasswordResetToken.create_for_user(
                user, minutes_valid=30
            )

            reset_url = request.build_absolute_uri(
                reverse("password_reset", args=[token_obj.token])
            )

            default_from_email = getattr(
                settings, "DEFAULT_FROM_EMAIL", "webmaster@localhost"
            )

            send_mail(
                subject="Password reset",
                message=(
                    "Reset your password using this link "
                    "(expires in 30 minutes):\n\n"
                    f"{reset_url}\n"
                ),
                from_email=default_from_email,
                recipient_list=[user.email],
                fail_silently=False,
            )

        return redirect("login")

    return render(request, "auth/password_forgot.html")


def password_reset_view(request, token: str):
    """
    Validate token, allow setting new password, mark token used.
    """
    token_obj = get_object_or_404(PasswordResetToken, token=token)

    # invalid if used or expired
    if token_obj.used_at is not None or timezone.now() > token_obj.expires_at:
        messages.error(request, "This reset link is invalid or has expired.")
        return redirect("password_forgot")

    if request.method == "POST":
        password1 = request.POST.get("password1", "")
        password2 = request.POST.get("password2", "")

        if not password1 or len(password1) < 8:
            messages.error(request, "Password must be at least 8 characters.")
            return render(
                request, "auth/password_reset.html", {"token": token}
            )

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(
                request, "auth/password_reset.html", {"token": token}
            )

        user = token_obj.user
        user.password = make_password(password1)
        user.save(update_fields=["password"])

        token_obj.used_at = timezone.now()
        token_obj.save(update_fields=["used_at"])

        messages.success(
            request,
            "Password reset successful. You can now log in."
        )
        return redirect("login")

    return render(request, "auth/password_reset.html", {"token": token})
