"""
shop.urls

URL routes for the shop app.
"""

from django.urls import path
from .views_auth import home_view, login_view, logout_view, register_view
from .views_public_products import public_product_detail
from .views_public_stores import public_store_list, public_store_detail
from .views_orders import my_orders
from .views_vendor_stores import (
    vendor_store_list,
    vendor_store_create,
    vendor_store_edit,
    vendor_store_delete,
)
from .views_vendor_products import (
    vendor_product_list,
    vendor_product_create,
    vendor_product_edit,
    vendor_product_delete,
)
from .views_cart import (
    cart_add,
    cart_detail,
    cart_remove,
    checkout,
    checkout_success,
)

from .views_password_reset import (
    password_forgot_view,
    password_reset_view,
)

urlpatterns = [
    # Home + auth
    path("", home_view, name="home"),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),

    # Vendor: stores
    path(
        "vendor/stores/",
        vendor_store_list,
        name="vendor_store_list"
    ),
    path(
        "vendor/stores/create/",
        vendor_store_create,
        name="vendor_store_create",
    ),
    path(
        "vendor/stores/<int:store_id>/edit/",
        vendor_store_edit,
        name="vendor_store_edit",
    ),
    path(
        "vendor/stores/<int:store_id>/delete/",
        vendor_store_delete,
        name="vendor_store_delete",
    ),

    # Vendor: products
    path(
        "vendor/stores/<int:store_id>/products/",
        vendor_product_list,
        name="vendor_product_list",
    ),
    path(
        "vendor/stores/<int:store_id>/products/create/",
        vendor_product_create,
        name="vendor_product_create",
    ),
    path(
        "vendor/stores/<int:store_id>/products/<int:product_id>/edit/",
        vendor_product_edit,
        name="vendor_product_edit",
    ),
    path(
        "vendor/stores/<int:store_id>/products/<int:product_id>/delete/",
        vendor_product_delete,
        name="vendor_product_delete",
    ),


    # Public: browse stores + products
    path(
        "stores/",
        public_store_list,
        name="public_store_list"
    ),
    path(
        "stores/<int:store_id>/",
        public_store_detail,
        name="public_store_detail",
    ),

    # Orders
    path(
        "orders/",
        my_orders,
        name="my_orders"
    ),

    # Cart
    path(
        "cart/",
        cart_detail,
        name="cart_detail"
    ),
    path(
        "cart/add/<int:product_id>/",
        cart_add,
        name="cart_add"
    ),
    path(
        "cart/remove/<int:product_id>/",
        cart_remove,
        name="cart_remove"
    ),
    path(
        "cart/checkout/",
        checkout,
        name="checkout"
    ),
    path(
        "cart/checkout/success/<int:order_id>/",
        checkout_success,
        name="checkout_success",
    ),

    # Public: product detail + reviews
    path(
        "products/<int:product_id>/",
        public_product_detail,
        name="public_product_detail"
    ),

    # Password reset
    path(
        "password/forgot/",
        password_forgot_view,
        name="password_forgot"
    ),
    path(
        "password/reset/<str:token>/",
        password_reset_view,
        name="password_reset"
    ),
]
