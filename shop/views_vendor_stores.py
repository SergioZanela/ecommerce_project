"""
shop.views_vendor_stores

Vendor-only views for managing stores (CRUD):
- vendor_store_list: list stores owned by the logged-in vendor
- vendor_store_create: create a new store
- vendor_store_edit: update an existing store owned by the vendor
- vendor_store_delete: delete a store owned by the vendor

Security:
    Uses @vendor_required and always filters by owner=request.user to prevent
    a vendor from editing/deleting another vendor's store.
"""

from django.contrib import messages
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render

from .forms import StoreForm
from .models import Store
from .permissions import vendor_required


@vendor_required
def vendor_store_list(request):
    """
    Display a list of stores owned by the logged-in vendor.

    Also includes basic dashboard stats:
        - total_stores
        - total_products (sum across stores)

    Returns:
        Rendered HTML page listing the vendor's stores.
    """
    stores = (
        Store.objects.filter(owner=request.user)
        .order_by("-created_at")
        .annotate(product_count=Count("products"))
    )

    total_stores = stores.count()
    total_products = sum(
        s.product_count for s in stores  # type: ignore[attr-defined]
    )

    return render(
        request,
        "shop/vendor/stores/list.html",
        {
            "stores": stores,
            "total_stores": total_stores,
            "total_products": total_products,
        },
    )


@vendor_required
def vendor_store_create(request):
    """
    Create a new store for the logged-in vendor.

    Behaviour:
        - GET: show empty StoreForm
        - POST: validate and save store with owner=request.user

    Returns:
        Rendered form page or redirect to the vendor store list on success.
    """
    if request.method == "POST":
        form = StoreForm(request.POST)
        if form.is_valid():
            store = form.save(commit=False)
            # critical security rule: owner is server-controlled
            store.owner = request.user
            store.save()
            messages.success(request, "Store created successfully.")
            return redirect("vendor_store_list")
    else:
        form = StoreForm()

    context = {"form": form, "mode": "create"}
    return render(request, "shop/vendor/stores/form.html", context)


@vendor_required
def vendor_store_edit(request, store_id: int):
    """
    Edit an existing store owned by the logged-in vendor.

    Args:
        store_id: ID of the store to edit.

    Security:
        Store is fetched using owner=request.user to prevent unauthorized
        edits.

    Returns:
        Rendered form page or redirect to the vendor store list on success.
    """
    store = get_object_or_404(Store, id=store_id, owner=request.user)

    if request.method == "POST":
        form = StoreForm(request.POST, instance=store)
        if form.is_valid():
            form.save()
            messages.success(request, "Store updated successfully.")
            return redirect("vendor_store_list")
    else:
        form = StoreForm(instance=store)

    context = {"form": form, "mode": "edit", "store": store}
    return render(request, "shop/vendor/stores/form.html", context)


@vendor_required
def vendor_store_delete(request, store_id: int):
    """
    Delete a store owned by the logged-in vendor.

    Args:
        store_id: ID of the store to delete.

    Behaviour:
        - GET: show confirmation page
        - POST: delete the store and redirect

    Returns:
        Confirmation page or redirect to the vendor store list after deletion.
    """
    store = get_object_or_404(Store, id=store_id, owner=request.user)

    if request.method == "POST":
        store.delete()
        messages.info(request, "Store deleted.")
        return redirect("vendor_store_list")

    context = {"store": store}
    return render(
        request, "shop/vendor/stores/confirm_delete.html", context
    )
