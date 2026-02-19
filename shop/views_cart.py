"""
shop.views_cart

Session-based cart + checkout:
- cart_detail: show cart contents
- cart_add: add a product to cart
- cart_remove: remove product from cart
- checkout: create Order/OrderItems, clear cart, email invoice
"""

from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect, render

from .models import Order, OrderItem, Product
from .permissions import buyer_required


def _get_cart(session) -> dict:
    """
    Cart stored in session as: {"<product_id>": quantity}
    """
    cart = session.get("cart")
    if not isinstance(cart, dict):
        cart = {}
        session["cart"] = cart
    return cart


def _cart_items(cart: dict):
    """
    Returns:
        items: list of dicts {product, quantity, line_total}
        total: Decimal
    """
    items = []
    total = Decimal("0.00")

    # Fetch products in one query
    product_ids = [int(pid) for pid in cart.keys()]
    products = Product.objects.filter(id__in=product_ids, is_active=True)

    products_by_id = {p.pk: p for p in products}

    for pid_str, qty in cart.items():
        pid = int(pid_str)
        product = products_by_id.get(pid)
        if not product:
            continue

        quantity = int(qty)
        line_total = (product.price or Decimal("0.00")) * quantity
        total += line_total

        items.append(
            {
                "product": product,
                "quantity": quantity,
                "line_total": line_total,
            }
        )

    return items, total


@buyer_required
def cart_detail(request):
    cart = _get_cart(request.session)
    items, total = _cart_items(cart)

    return render(
        request,
        "shop/cart/detail.html",
        {"items": items, "total": total},
    )


@buyer_required
def cart_add(request, product_id: int):
    product = get_object_or_404(Product, id=product_id, is_active=True)

    cart = _get_cart(request.session)
    key = str(product.pk)

    cart[key] = int(cart.get(key, 0)) + 1
    request.session["cart"] = cart
    request.session.modified = True

    messages.success(request, f"Added '{product.name}' to your cart.")
    return redirect("public_store_detail", store_id=product.store.pk)


@buyer_required
def cart_remove(request, product_id: int):
    cart = _get_cart(request.session)
    key = str(product_id)

    if key in cart:
        del cart[key]
        request.session["cart"] = cart
        request.session.modified = True
        messages.info(request, "Item removed from cart.")

    return redirect("cart_detail")


@buyer_required
def checkout(request):
    """
    Creates an Order + OrderItems from session cart, clears cart,
    and emails invoice (with attachment).
    """
    cart = _get_cart(request.session)
    items, total = _cart_items(cart)

    if not items:
        messages.error(request, "Your cart is empty.")
        return redirect("cart_detail")

    if not request.user.email:
        messages.error(
            request,
            "Please add an email address to your account before checkout.",
        )
        return redirect("cart_detail")

    # Create order
    order = Order.objects.create(
        buyer=request.user,
        email_sent=False,
    )

    # Create order items with snapshots
    for item in items:
        p = item["product"]
        OrderItem.objects.create(
            order=order,
            product=p,
            quantity=item["quantity"],
            product_name_snapshot=p.name,
            price_snapshot=p.price,
        )

    # Clear cart
    request.session["cart"] = {}
    request.session.modified = True

    # Build invoice text (for body + attachment)
    lines = []
    lines.append(f"INVOICE for Order #{order.id}")
    lines.append(f"Customer: {request.user.username} ({request.user.email})")
    lines.append("")
    lines.append("Items:")

    for item in items:
        p = item["product"]
        qty = item["quantity"]
        price = p.price
        line_total = item["line_total"]
        lines.append(f"- {p.name} (x{qty}) @ ${price} = ${line_total}")

    lines.append("")
    lines.append(f"TOTAL: ${total}")
    lines.append("")
    lines.append("Thank you for your purchase!")

    invoice_text = "\n".join(lines)

    # ✅ Email with attachment so you can "see" the invoice file
    subject = f"Your Invoice - Order #{order.id}"
    email = EmailMessage(
        subject=subject,
        body="Thanks for your order! Your invoice is attached.",
        from_email=None,  # uses DEFAULT_FROM_EMAIL
        to=[request.user.email],
    )

    email.attach(
        filename=f"invoice_order_{order.id}.txt",
        content=invoice_text,
        mimetype="text/plain",
    )

    email.send(fail_silently=False)

    order.email_sent = True
    order.save(update_fields=["email_sent"])

    messages.success(request, "Checkout complete! Invoice sent to your email.")
    return redirect("checkout_success", order_id=order.id)


@login_required
def checkout_success(request, order_id: int):
    # buyer can only view their own order
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    order_items = OrderItem.objects.filter(
        order=order
    ).select_related("product")
    return render(
        request,
        "shop/cart/checkout_success.html",
        {"order": order, "order_items": order_items},
    )
