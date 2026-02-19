"""
shop.apps

AppConfig for the shop app.
"""

from django.apps import AppConfig


class ShopConfig(AppConfig):
    """Configuration for the shop Django app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "shop"

    def ready(self) -> None:
        """
        Import signal handlers when the app is ready.
        """
        from . import signals  # noqa: F401
