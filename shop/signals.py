"""
shop.signals

Signal handlers for the shop app.

Currently:
- Ensures every User has a related Profile instance.
"""

from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    """
    Create a Profile automatically when a new User is created.

    Args:
        sender: The model class sending the signal (User).
        instance: The saved User instance.
        created: True if the instance was created on this save.
        **kwargs: Extra signal kwargs.

    Notes:
        We default role to buyer; registration view can overwrite it.
    """
    if created:
        Profile.objects.create(user=instance, role=Profile.ROLE_BUYER)
