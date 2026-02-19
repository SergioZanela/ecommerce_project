# 🧠 Project Planning — Django eCommerce Application

## Project Overview

This project aims to build a multi-role eCommerce web application using Django.

The system will support:

- Buyers browsing stores and purchasing products
- Vendors managing stores and products
- Cart and checkout functionality
- Reviews and ratings
- Basic dashboard insights

The project follows a simple iterative development approach.

---

# 🎯 Goals

## Core Functional Goals

### Authentication
- User registration
- Login / logout
- Role-based users (buyer / vendor)

### Buyer Features
- View stores
- View products
- Add products to cart
- Checkout process
- View order history
- Leave product reviews

### Vendor Features
- Create stores
- Manage products (CRUD)
- Vendor-only access protection

### Order System
- Create orders at checkout
- Store product snapshots (name + price)
- Generate invoice email

---

## Extended Goals (Enhancements)

Planned improvements after core system:

1. Product search
2. Pagination for large product lists
3. Average rating per store
4. Vendor dashboard statistics
5. Improved UI styling using CSS

---

# 🏗 Architecture Plan

## Separation of Views

To keep code maintainable, views will be split:

- `views_public_*` → Public browsing logic
- `views_vendor_*` → Vendor dashboard & CRUD
- `views_cart.py` → Cart and checkout
- `views_auth.py` → Authentication logic
- `views_password_reset.py` → Password reset workflow
- `views_orders.py` → Buyer order history

---

## Database Design (High Level)

### Main Models

- User (Django auth)
- Profile (role information)
- Store
- Product
- Order
- OrderItem
- Review
- PasswordResetToken

### Relationships

- Vendor → owns Stores
- Store → has Products
- Buyer → creates Orders
- Order → contains OrderItems
- Product → has Reviews

---

# 🔐 Security Planning

- Vendor-only pages protected by decorators
- All vendor queries filtered by `owner=request.user`
- Buyers cannot edit vendor resources
- Password reset tokens expire automatically

---

# 🛒 Cart Design

Cart will be stored in Django session:

- {product_id: quantity}
- Cart view will calculate total price on the fly
- Checkout will create Order and clear cart

# 📧 Email Design

- Order confirmation emails
- Password reset emails
- Vendor notifications for new orders
- Use Django's email framework with console backend for development

# 🧪 Testing Plan

- Unit tests for models
- Integration tests for views
- Functional tests for user workflows
- Use Django's test framework with in-memory SQLite database
- Test coverage for authentication, cart, checkout, and vendor management

# 🚀 Deployment Plan

- Use Django's built-in deployment checklist
- Configure production settings (DEBUG=False, ALLOWED_HOSTS, etc.)
- Use a production-ready database (PostgreSQL)
- Serve static files with WhiteNoise or a CDN
- Deploy on a cloud platform (Heroku, AWS, etc.)
- Set up environment variables for sensitive settings (SECRET_KEY, database credentials)
- Use a WSGI server (Gunicorn) for production deployment

# 🗓 Development Phases (Planned)

## Phase 1 — Core Setup
- Models
- Authentication
- Role system

## Phase 2 — Vendor CRUD
- Stores
- Products

## Phase 3 — Buyer Experience
- Public browsing
- Cart and checkout

## Phase 4 — Enhancements
- Reviews
- Search
- Pagination
- Ratings
- Dashboard stats

## Phase 5 — UI & Polish
- CSS styling
- Base template
- Documentation (README)
