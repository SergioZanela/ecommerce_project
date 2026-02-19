"""
shop.models

Database models for the eCommerce application.

This module defines:
- Profile: stores the user's role (vendor/buyer)
- Store: vendor-owned store
- Product: items sold in stores
- Order / OrderItem: checkout records (used later for invoices +
  verified reviews)
- Review: product reviews with verified/unverified status
- PasswordResetToken: expiring tokens for password reset emails
"""

from __future__ import annotations

import secrets
from datetime import timedelta
from decimal import Decimal

from django.conf import settings
from django.db import models
from django.utils import timezone


class Profile(models.Model):
    """
    Extends the built-in Django User model with an application role.

    Roles:
        - vendor: can create/manage stores and products
        - buyer: can browse, add to cart, checkout, and review products

    Attributes:
        user: One-to-one link to the Django auth user.
        role: Role string ("vendor" or "buyer").
    """

    ROLE_VENDOR = "vendor"
    ROLE_BUYER = "buyer"
    ROLE_CHOICES = [(ROLE_VENDOR, "Vendor"), (ROLE_BUYER, "Buyer")]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self) -> str:
        """Return a readable identifier for admin/debugging."""
        return f"{self.user.username} ({self.role})"


"""
This module contains:
- Profile: Extends Django's User with a role (vendor or buyer)
- Store: A vendor-owned store that contains products (added later)
"""


class Store(models.Model):
    """
    Represents a store owned by a vendor.

    Each store belongs to exactly one user (the vendor). A vendor may own
    multiple stores. Buyers can browse stores to view their products.

    Fields:
        owner: The user who owns this store (must be a vendor).
        name: Public-facing store name.
        description: Optional details about what the store sells.
        created_at: When the store was created.
        updated_at: When the store was last modified.
    """

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="stores",
        help_text="The vendor account that owns this store.",
    )
    name = models.CharField(
        max_length=120, help_text="The store's display name."
    )
    description = models.TextField(
        blank=True, help_text="Optional store description."
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Creation timestamp."
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Last update timestamp."
    )

    class Meta:
        ordering = ["-created_at"]
        # Optional: prevents a vendor from having 2 stores with the
        # exact same name
        unique_together = ("owner", "name")

    def __str__(self) -> str:
        """
        Return a readable string for admin/debugging.

        Returns:
            Store name string.
        """
        return self.name


class Product(models.Model):
    """
    Represents a product listed inside a store.

    Attributes:
        store: The store this product belongs to.
        name: Product name.
        description: Product description.
        price: Product price (decimal).
        is_active: Whether the product is visible to buyers.
        created_at: Timestamp of creation.
    """

    store = models.ForeignKey(
        Store,
        on_delete=models.CASCADE,
        related_name="products",
    )
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return product name."""
        return self.name


class Order(models.Model):
    """
    Represents a completed checkout by a buyer.
    """

    id = models.BigAutoField(primary_key=True)
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False)

    def __str__(self) -> str:
        """Return a readable order label."""
        return f"Order #{self.id} by {self.buyer.username}"


class OrderItem(models.Model):
    """
    Represents an item line inside an Order.

    Important:
        We store snapshots of product name and price so the invoice remains
        accurate even if the vendor changes the product later.

    Attributes:
        order: Parent order.
        product: Purchased product.
        quantity: Number of units purchased.
        product_name_snapshot: Product name at purchase time.
        price_snapshot: Product price at purchase time.
    """

    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    product_name_snapshot = models.CharField(max_length=150)
    price_snapshot = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self) -> str:
        return (
            f"OrderItem(order={self.order.pk}, "
            f"product={self.product.pk}, qty={self.quantity})"
        )

    def line_total(self) -> Decimal:
        """Calculate total price for this line item."""
        return self.quantity * self.price_snapshot


class Review(models.Model):
    """
    Represents a review left by a user for a product.

    Verified vs Unverified:
        A review is "verified" if the reviewer has purchased the product
        before. Otherwise it is unverified (still allowed by the assignment
        requirements).

    Attributes:
        product: Product being reviewed.
        author: User who wrote the review.
        rating: Integer rating (1-5).
        comment: Review text.
        verified: Whether the reviewer purchased the product.
        created_at: Timestamp of review creation.
    """

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="reviews",
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        """Return short label for admin/debug."""
        return f"Review({self.product.pk}) by {self.author.username}"


class PasswordResetToken(models.Model):
    """
    Stores expiring password reset tokens.

    Security behaviour:
        - tokens expire after a configured window (default 30 minutes)
        - tokens can only be used once

    Attributes:
        user: User requesting password reset.
        token: Random token string (URL-safe).
        expires_at: Expiry datetime.
        used_at: Datetime token was used (null means unused).
        created_at: Timestamp when token was created.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )
    token = models.CharField(max_length=128, unique=True)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @classmethod
    def create_for_user(
        cls, user, minutes_valid: int = 30
    ) -> "PasswordResetToken":
        """
        Create and store a new password reset token.

        Args:
            user: The user requesting the reset.
            minutes_valid: How long the token stays valid.

        Returns:
            The created PasswordResetToken instance.
        """
        token_value = secrets.token_urlsafe(32)
        expires = timezone.now() + timedelta(minutes=minutes_valid)
        return cls.objects.create(
            user=user, token=token_value, expires_at=expires
        )

    def is_valid(self) -> bool:
        """
        Check if the token is valid for use.

        Returns:
            True if unused and not expired; otherwise False.
        """
        if self.used_at is not None:
            return False
        return timezone.now() < self.expires_at

    def __str__(self) -> str:
        """Return a readable label for admin/debug."""
        status = "used" if self.used_at else "active"
        return (
            f"PasswordResetToken(user={self.user.id}, {status}, "
            f"expires={self.expires_at})"
        )
