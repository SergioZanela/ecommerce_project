from django.test import TestCase, override_settings
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import (
    Profile,
    Store,
    Product,
    Order,
    OrderItem,
    PasswordResetToken,
)

User = get_user_model()


class BaseTestHelpers(TestCase):
    def create_user(self, username: str, email: str, password: str, role: str):
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )
        # profile is created by signals; set role explicitly
        profile = Profile.objects.get(user=user)
        profile.role = role
        profile.save(update_fields=["role"])
        return user

    def login(self, user, password: str):
        ok = self.client.login(username=user.username, password=password)
        self.assertTrue(ok)


class VendorStoreProductTests(BaseTestHelpers):
    def test_vendor_can_create_store(self):
        vendor = self.create_user(
            "vendor1", "vendor1@test.com", "pass12345", Profile.ROLE_VENDOR
        )
        self.login(vendor, "pass12345")

        resp = self.client.post(
            reverse("vendor_store_create"),
            {"name": "My Store", "description": "Test store"},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        store_exists = Store.objects.filter(
            owner=vendor, name="My Store"
        ).exists()
        self.assertTrue(store_exists)

    def test_vendor_can_create_product_in_own_store(self):
        vendor = self.create_user(
            "vendor2", "vendor2@test.com", "pass12345", Profile.ROLE_VENDOR
        )
        self.login(vendor, "pass12345")

        store = Store.objects.create(owner=vendor, name="S1", description="")

        resp = self.client.post(
            reverse("vendor_product_create", kwargs={"store_id": store.pk}),
            {
                "name": "P1",
                "description": "Prod",
                "price": "19.99",
                "is_active": True,
            },
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)
        product_exists = Product.objects.filter(
            store=store, name="P1"
        ).exists()
        self.assertTrue(product_exists)

    def test_buyer_cannot_access_vendor_pages(self):
        buyer = self.create_user(
            "buyer1", "buyer1@test.com", "pass12345", Profile.ROLE_BUYER
        )
        self.login(buyer, "pass12345")

        resp = self.client.get(reverse("vendor_store_list"), follow=True)
        self.assertEqual(resp.status_code, 200)
        # buyer_required redirects home for wrong role
        self.assertTrue(resp.redirect_chain)  # proves redirect happened


class CartCheckoutTests(BaseTestHelpers):
    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
    )
    def test_buyer_can_add_to_cart_and_checkout_creates_order(self):
        vendor = self.create_user(
            "vendor3", "vendor3@test.com", "pass12345", Profile.ROLE_VENDOR
        )
        store = Store.objects.create(
            owner=vendor, name="Store", description=""
        )
        product = Product.objects.create(
            store=store,
            name="Widget",
            description="",
            price="10.00",
            is_active=True,
        )

        buyer = self.create_user(
            "buyer2", "buyer2@test.com", "pass12345", Profile.ROLE_BUYER
        )
        self.login(buyer, "pass12345")

        # add to cart
        resp = self.client.get(
            reverse("cart_add", kwargs={"product_id": product.pk}),
            follow=True
        )
        self.assertEqual(resp.status_code, 200)

        # checkout
        resp = self.client.get(reverse("checkout"), follow=True)
        self.assertEqual(resp.status_code, 200)

        # order created
        order = Order.objects.filter(buyer=buyer).order_by("-id").first()
        self.assertIsNotNone(order)

        items = OrderItem.objects.filter(order=order)
        self.assertEqual(items.count(), 1)
        item = items.first()
        self.assertIsNotNone(item)
        if item is not None:
            self.assertEqual(item.product, product)
            self.assertEqual(item.quantity, 1)

    def test_vendor_cannot_access_cart_pages(self):
        vendor = self.create_user(
            "vendor4", "vendor4@test.com", "pass12345", Profile.ROLE_VENDOR
        )
        self.login(vendor, "pass12345")

        resp = self.client.get(reverse("cart_detail"), follow=True)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.redirect_chain)  # redirected to home


class PasswordResetTests(BaseTestHelpers):
    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
    )
    def test_password_forgot_creates_token_for_existing_email(self):
        user = self.create_user(
            "buyer3", "buyer3@test.com", "pass12345", Profile.ROLE_BUYER
        )

        resp = self.client.post(
            reverse("password_forgot"),
            {"email": user.email},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)

        token_obj = (
            PasswordResetToken.objects.filter(user=user)
            .order_by("-id")
            .first()
        )
        self.assertIsNotNone(token_obj)

        # Token must exist and be non-empty
        if token_obj is not None:
            self.assertTrue(bool(token_obj.token))

    @override_settings(
        EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend"
    )
    def test_password_forgot_does_not_create_token_for_nonexistent_email(self):
        resp = self.client.post(
            reverse("password_forgot"),
            {"email": "nonexistent@test.com"},
            follow=True,
        )
        self.assertEqual(resp.status_code, 200)

        token_obj = (
            PasswordResetToken.objects.filter(
                user__email="nonexistent@test.com"
            )
            .order_by("-id")
            .first()
        )
        self.assertIsNone(token_obj)
