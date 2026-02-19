from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from .models import Order


@login_required
def my_orders(request):
    """
    Buyer: list their own orders (newest first).
    Vendors can access but will only see orders where they are
    the buyer (usually none).
    """
    orders = (
        Order.objects.filter(buyer=request.user)
        .order_by("-created_at")
        .prefetch_related("items")
    )

    return render(request, "orders/my_orders.html", {"orders": orders})
