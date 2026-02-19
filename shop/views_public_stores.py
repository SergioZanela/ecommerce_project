"""
shop.views_public_stores

Public views:
- public_store_list: list all active stores
- public_store_detail: show one store + its active products
"""

from django.core.paginator import Paginator
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, render

from .models import Product, Store


def public_store_list(request):
    stores = Store.objects.order_by("-created_at")
    return render(request, "shop/public/stores/list.html", {"stores": stores})


def public_store_detail(request, store_id):
    store = get_object_or_404(Store, id=store_id)

    q = request.GET.get("q", "").strip()

    products_qs = Product.objects.filter(store=store, is_active=True)

    if q:
        products_qs = products_qs.filter(
            Q(name__icontains=q) | Q(description__icontains=q)
        )

    products_qs = products_qs.order_by("name")

    paginator = Paginator(products_qs, 6)  # 6 products per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    average_rating = (
        Product.objects.filter(store=store, reviews__isnull=False)
        .aggregate(avg=Avg("reviews__rating"))["avg"]
    )

    return render(
        request,
        "shop/public/stores/detail.html",
        {
            "store": store,
            "products": page_obj.object_list,
            "page_obj": page_obj,
            "average_rating": average_rating,
        },
    )
