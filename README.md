# 🛍 Django eCommerce Application

A full-featured eCommerce web application built with Django.

This project supports:

- Buyers and Vendors (role-based access)
- Vendor store & product management
- Product browsing with search and pagination
- Shopping cart & checkout system
- Order history (My Orders)
- Product reviews with verified purchase flag
- Store average rating calculation
- Vendor dashboard statistics
- Password reset with expiring tokens
- Unit testing

---

# 🚀 Features

## 👤 Authentication & Roles
- User registration and login
- Role selection (Buyer or Vendor)
- Role-based permissions using decorators
- Password reset with secure token expiration

---

## 🛒 Buyer Features
- Browse all stores
- View products in a store
- 🔍 Search products within a store
- 📄 Paginated product listings
- Add products to cart
- Checkout and generate order
- 🧾 View order history ("My Orders")
- Leave product reviews
- Verified purchase flag on reviews

---

## 🏪 Vendor Features
- Vendor dashboard
- Create / edit / delete stores
- Create / edit / delete products
- 📊 Vendor statistics:
  - Total stores
  - Total products

---

## ⭐ Store Enhancements
- Store average rating calculation
- Displays rating with 1 decimal precision
- Handles “No ratings yet” case

---

## ✉ Email
- Checkout invoice email (console backend in development)
- Password reset email (console backend)

---

# 🏗 Architecture Overview

Views are separated by responsibility:

- `views_public_*` → Public browsing
- `views_vendor_*` → Vendor dashboard
- `views_cart.py` → Cart & checkout
- `views_orders.py` → Buyer order history
- `views_password_reset.py` → Password reset system

Cart is session-based.

Orders store **product snapshots** to ensure historical accuracy even if products are edited later.

---

## 📁 Project Structure

ecommerce_project/
│
├── manage.py
├── requirements.txt
├── README.md
│
├── ecommerce_project/
│ ├── settings.py
│ ├── urls.py
│ └── ...
│
└── shop/
├── models.py
├── views_auth.py
├── views_public_products.py
├── views_public_stores.py
├── views_vendor_products.py
├── views_vendor_stores.py
├── views_cart.py
├── views_orders.py
├── views_password_reset.py
├── forms.py
├── permissions.py
├── tests.py
│
├── static/
│ └── shop/
│ └── style.css
│
└── templates/
├── base.html
├── auth/
├── shop/
│ ├── public/
│ ├── vendor/
│ └── cart/
└── orders/

---

# ⚙ Installation

## 1️⃣ Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # macOS/Linux
```
