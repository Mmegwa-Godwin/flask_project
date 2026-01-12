from flask import Blueprint, render_template, redirect, url_for, flash, session, g, has_request_context
from flask_login import login_required, current_user # pyright: ignore[reportMissingImports]
from extensions import db
from models.product import Product
from models.cart import Cart, CartItem
from models.order import Order, OrderItem
from functools import wraps

shop_bp = Blueprint("shop", __name__)

# ---------------------------
# Admin Access Decorator (example)
# ---------------------------
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not getattr(current_user, "is_authenticated", False) or not getattr(current_user, "is_admin", False):
            flash("Admin access required.", "danger")
            return redirect(url_for("admin.admin_login"))
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------
# Home / Products
# ---------------------------
@shop_bp.route("/")
def index():
    products = Product.query.all()
    return render_template("shop/index.html", products=products)

# ---------------------------
# Add to Cart
# ---------------------------
@shop_bp.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
    if hasattr(current_user, "is_authenticated") and current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if not cart:
            cart = Cart(user=current_user)
            db.session.add(cart)
            db.session.commit()

        item = next((i for i in cart.items if i.product_id == product_id), None)
        if item:
            item.quantity += 1
        else:
            db.session.add(CartItem(cart_id=cart.id, product_id=product_id, quantity=1))
        db.session.commit()
    else:
        # Guest cart in session
        cart = session.get("cart", {})
        cart[str(product_id)] = cart.get(str(product_id), 0) + 1
        session["cart"] = cart

    flash("Item added to cart", "success")
    return redirect(url_for("shop.index"))

# ---------------------------
# View Cart
# ---------------------------
@shop_bp.route("/cart")
def cart():
    products = []
    total = 0

    if hasattr(current_user, "is_authenticated") and current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            for item in cart.items:
                products.append({"product": item.product, "quantity": item.quantity})
                total += item.product.price * item.quantity
    else:
        session_cart = session.get("cart", {})
        for pid, qty in session_cart.items():
            product = db.session.get(Product, int(pid))
            if product:
                products.append({"product": product, "quantity": qty})
                total += product.price * qty

    return render_template("shop/cart.html", products=products, total=total)

# ---------------------------
# Load cart count for nav
# ---------------------------
@shop_bp.before_app_request
def load_cart_count():
    g.cart_count = 0
    if not has_request_context() or not hasattr(current_user, "is_authenticated"):
        return

    if current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            g.cart_count = sum(item.quantity for item in cart.items)
    else:
        session_cart = session.get("cart", {})
        g.cart_count = sum(session_cart.values())

# ---------------------------
# Remove Item from Cart
# ---------------------------
@shop_bp.route('/remove_from_cart/<int:product_id>')
@login_required
def remove_from_cart(product_id):
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if cart:
        item = CartItem.query.filter_by(cart_id=cart.id, product_id=product_id).first()
        if item:
            db.session.delete(item)
            db.session.commit()
            flash("Product removed from cart!", "info")
    return redirect(url_for('shop.cart'))

# ---------------------------
# Checkout
# ---------------------------
@shop_bp.route("/checkout")
@login_required
def checkout():
    cart = Cart.query.filter_by(user_id=current_user.id).first()
    if not cart or not cart.items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("shop.index"))

    order = Order(user=current_user, total_amount=0)
    db.session.add(order)
    db.session.commit()

    total = 0
    for item in cart.items:
        total += item.product.price * item.quantity
        db.session.add(OrderItem(
            order_id=order.id,
            product_id=item.product.id,
            quantity=item.quantity,
            price=item.product.price
        ))
        db.session.delete(item)

    order.total_amount = total
    db.session.commit()

    flash("Order placed successfully!", "success")
    return redirect(url_for("shop.orders"))

# ---------------------------
# User Orders
# ---------------------------
@shop_bp.route("/orders")
@login_required
def orders():
    orders = current_user.orders
    orders = sorted(orders, key=lambda o: o.created_at, reverse=True)
    return render_template("shop/orders.html", orders=orders)

# ---------------------------
# Mock Payment
# ---------------------------
@shop_bp.route("/pay/<int:order_id>")
@login_required
def pay(order_id):
    order = db.session.get(Order, order_id)
    if not order or order.user != current_user:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("shop.orders"))

    # Mock payment: mark as paid
    order.status = "Paid"
    db.session.commit()
    flash("Payment successful (mock).", "success")
    return redirect(url_for("shop.orders"))
