"""
shop.views_vendor_products

Vendor-only views for managing products within a store (CRUD):
- vendor_product_list: list products for a store owned by the logged-in vendor
- vendor_product_create: create a product under a store owned by the vendor
- vendor_product_edit: update a product under a store owned by the vendor
- vendor_product_delete: delete a product under a store owned by the vendor

Security:
- Uses @vendor_required
- Always checks store.owner == request.user
"""

from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductForm
from .models import Product, Store
from .permissions import vendor_required


@vendor_required
def vendor_product_list(request, store_id: int):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    products = Product.objects.filter(store=store).order_by("-created_at")
    return render(
        request,
        "shop/vendor/products/list.html",
        {"store": store, "products": products},
    )


@vendor_required
def vendor_product_create(request, store_id: int):
    store = get_object_or_404(Store, id=store_id, owner=request.user)

    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.store = store  # server-controlled
            product.save()
            messages.success(request, "Product created successfully.")
            return redirect("vendor_product_list", store_id=store.pk)
    else:
        form = ProductForm()

    return render(
        request,
        "shop/vendor/products/form.html",
        {"form": form, "mode": "create", "store": store},
    )


@vendor_required
def vendor_product_edit(request, store_id: int, product_id: int):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    product = get_object_or_404(Product, id=product_id, store=store)

    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("vendor_product_list", store_id=store.pk)
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "shop/vendor/products/form.html",
        {"form": form, "mode": "edit", "store": store, "product": product},
    )


@vendor_required
def vendor_product_delete(request, store_id: int, product_id: int):
    store = get_object_or_404(Store, id=store_id, owner=request.user)
    product = get_object_or_404(Product, id=product_id, store=store)

    if request.method == "POST":
        product.delete()
        messages.info(request, "Product deleted.")
        return redirect("vendor_product_list", store_id=store.pk)

    return render(
        request,
        "shop/vendor/products/confirm_delete.html",
        {"store": store, "product": product},
    )
