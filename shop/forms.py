"""
shop.forms

Contains Django forms used to register users and capture their role
(buyer/vendor) during account creation.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Product, Profile, Store, Review


class RegisterForm(UserCreationForm):
    """
    User registration form that extends Django's built-in UserCreationForm.

    Adds a `role` field so users can choose to register as a buyer or vendor.
    """

    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)

    class Meta:
        """
        Form metadata describing which User model fields are displayed.
        """
        model = User
        fields = ("username", "email", "role", "password1", "password2")


class StoreForm(forms.ModelForm):
    """
    Form used by vendors to create and edit stores.

    Notes:
        - The `owner` field is NOT exposed in the form.
        - The view sets `store.owner = request.user` to prevent tampering.
    """

    class Meta:
        model = Store
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(
                attrs={"placeholder": "Store name"}
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Describe your store (optional)",
                }
            ),
        }


class ProductForm(forms.ModelForm):
    """
    Form used by vendors to create and edit products.

    Notes:
        - The `store` field is NOT exposed in the form.
        - The view sets `product.store = store` to prevent tampering.
    """

    class Meta:
        model = Product
        fields = ["name", "description", "price", "is_active"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Product name"}),
            "description": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Product description"}
            ),
        }


class ReviewForm(forms.ModelForm):
    """
    Form used by buyers to leave a review on a product.
    """

    class Meta:
        model = Review
        fields = ["rating", "comment"]
        widgets = {
            "rating": forms.NumberInput(attrs={"min": 1, "max": 5}),
            "comment": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Write your review...",
                }
            ),
        }
