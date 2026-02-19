"""
shop.views_vendor

Vendor-specific views:
- manage stores
"""

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Store
from .permissions import vendor_required


@login_required
@vendor_required
def vendor_store_list(request):
    """
    Display stores owned by the logged-in vendor.
    """
    stores = Store.objects.filter(owner=request.user)

    return render(
        request,
        "shop/vendor/store_list.html",
        {"stores": stores},
    )
