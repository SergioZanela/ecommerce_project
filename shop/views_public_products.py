"""
shop.views_public_products

Public product views:
- public_product_detail: show a product + reviews, allow buyers to post reviews
"""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ReviewForm
from .models import OrderItem, Product, Review


def public_product_detail(request, product_id: int):
    product = get_object_or_404(Product, id=product_id, is_active=True)

    reviews = Review.objects.filter(product=product).order_by("-created_at")

    form = ReviewForm()

    # Handle review POST
    if request.method == "POST":
        if not request.user.is_authenticated:
            messages.error(
                request,
                "You must be logged in as a buyer to leave a review."
            )
            return redirect("login")

        # role check (buyer only)
        try:
            role = request.user.profile.role
        except Exception:
            role = None

        if role != "buyer":
            messages.error(request, "Only buyers can leave reviews.")
            return redirect("public_product_detail", product_id=product.pk)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.author = request.user

            # VERIFIED if buyer has purchased this product before
            purchased = OrderItem.objects.filter(
                order__buyer=request.user,
                product=product,
            ).exists()
            review.verified = purchased

            review.save()
            messages.success(request, "Review posted.")
            return redirect("public_product_detail", product_id=product.pk)

    return render(
        request,
        "shop/public/products/detail.html",
        {"product": product, "reviews": reviews, "form": form},
    )
