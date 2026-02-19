"""
shop.admin

Admin site configuration for the eCommerce application.

Registers models so an admin user can manage:
- user profiles (roles)
- stores and products
- orders and order items
- reviews
- password reset tokens
"""

from django.contrib import admin

from .models import (
    Order,
    OrderItem,
    PasswordResetToken,
    Product,
    Profile,
    Review,
    Store,
)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin display configuration for Profile records.
    """
    list_display = ("user", "role")
    list_filter = ("role",)
    search_fields = ("user__username", "user__email")


@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    """
    Admin display configuration for Store records.
    """
    list_display = ("name", "owner", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "owner__username")


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    """
    Admin display configuration for Product records.
    """
    list_display = ("name", "store", "price", "is_active", "created_at")
    list_filter = ("is_active", "created_at", "store")
    search_fields = ("name", "store__name")


class OrderItemInline(admin.TabularInline):
    """
    Inline order items shown within an Order page.
    """
    model = OrderItem
    extra = 0
    readonly_fields = (
        "product",
        "quantity",
        "product_name_snapshot",
        "price_snapshot",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """
    Admin display configuration for Order records.
    """
    list_display = ("id", "buyer", "created_at", "email_sent")
    list_filter = ("created_at", "email_sent")
    search_fields = ("buyer__username", "buyer__email")
    inlines = [OrderItemInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    """
    Admin display configuration for Review records.
    """
    list_display = ("product", "author", "rating", "verified", "created_at")
    list_filter = ("verified", "rating", "created_at")
    search_fields = ("product__name", "author__username")


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """
    Admin display configuration for PasswordResetToken records.

    Note:
        In a real production app you might not expose tokens in admin,
        but for a class project it's useful for debugging.
    """
    list_display = ("user", "token", "expires_at", "used_at", "created_at")
    list_filter = ("expires_at", "used_at", "created_at")
    search_fields = ("user__username", "user__email", "token")
