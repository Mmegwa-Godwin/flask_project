from flask import Blueprint, render_template, redirect, url_for, flash, session, g, request, has_request_context
from flask_login import login_required, current_user
from extensions import db
from models.product import Product
from models.cart import Cart, CartItem
from models.order import Order, OrderItem
<<<<<<< HEAD
=======
from extensions import db
import requests
from flask import has_request_context
>>>>>>> 1ffaa6aa9f9629ca5a1ba5494dcad47d2fee9c95

shop_bp = Blueprint("shop", __name__)

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
<<<<<<< HEAD
    if current_user.is_authenticated:
        cart = current_user.cart
=======
    if hasattr(current_user, "is_authenticated") and current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
>>>>>>> 1ffaa6aa9f9629ca5a1ba5494dcad47d2fee9c95
        if not cart:
            cart = Cart(user=current_user)
            db.session.add(cart)
            db.session.commit()

        item = next((i for i in cart.items_in_cart if i.product_id == product_id), None)
        if item:
            item.quantity += 1
        else:
<<<<<<< HEAD
            cart.items_in_cart.append(CartItem(product_id=product_id, quantity=1))
=======
            db.session.add(CartItem(cart_id=cart.id, product_id=product_id, quantity=1))
>>>>>>> 1ffaa6aa9f9629ca5a1ba5494dcad47d2fee9c95
        db.session.commit()
    else:
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

<<<<<<< HEAD
    if current_user.is_authenticated:
        cart = current_user.cart
        if cart:
            for item in cart.items_in_cart:
                products.append({"product": item.product, "quantity": item.quantity})
                total += item.product.price * item.quantity
    else:
        session_cart = session.get("cart", {})
        for pid, qty in session_cart.items():
            product = db.session.get(Product, int(pid))
            if product:
                products.append({"product": product, "quantity": qty})
=======
    if hasattr(current_user, "is_authenticated") and current_user.is_authenticated:
        cart = Cart.query.filter_by(user_id=current_user.id).first()
        if cart:
            for item in cart.items:
                products_in_cart.append({"product": item.product, "quantity": item.quantity})
                total += item.product.price * item.quantity
    else:
        session_cart = session.get("cart", {})
        for product_id, qty in session_cart.items():
            product = db.session.get(Product, int(product_id))
            if product:
                products_in_cart.append({"product": product, "quantity": qty})
>>>>>>> 1ffaa6aa9f9629ca5a1ba5494dcad47d2fee9c95
                total += product.price * qty

    return render_template("shop/cart.html", products=products, total=total)

# ---------------------------
# Cart Count
# ---------------------------

# Wrap the existing hook
def safe_before_app_request(fn):
    def wrapper(*args, **kwargs):
        if not has_request_context():
            return  # skip if no request (Render safe)
        return fn(*args, **kwargs)
    return wrapper
    
@shop_bp.before_app_request
def load_cart_count():
    g.cart_count = 0
<<<<<<< HEAD
    if not has_request_context():
        return
    try:
        if current_user.is_authenticated:
            cart = current_user.cart
            if cart:
                g.cart_count = sum(item.quantity for item in cart.items_in_cart)
        else:
            g.cart_count = sum(session.get("cart", {}).values())
    except Exception:
        g.cart_count = 0
=======
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
>>>>>>> 1ffaa6aa9f9629ca5a1ba5494dcad47d2fee9c95

# ---------------------------
# Checkout
# ---------------------------
@shop_bp.route("/checkout")
@login_required
def checkout():
    cart = current_user.cart
    if not cart or not cart.items_in_cart:
        flash("Your cart is empty.", "warning")
        return redirect(url_for("shop.index"))

    order = Order(user=current_user, total_amount=0)
    db.session.add(order)
    db.session.commit()

    total = 0
    for item in cart.items_in_cart:
        total += item.product.price * item.quantity
<<<<<<< HEAD
        db.session.add(OrderItem(order=order, product=item.product, quantity=item.quantity, price=item.product.price))
=======
        db.session.add(OrderItem(
            order_id=order.id,
            product_id=item.product.id,
            quantity=item.quantity,
            price=item.product.price
        ))
>>>>>>> 1ffaa6aa9f9629ca5a1ba5494dcad47d2fee9c95
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
<<<<<<< HEAD
# Mock Payment
=======
# Opay Payment (Render Safe)
>>>>>>> 1ffaa6aa9f9629ca5a1ba5494dcad47d2fee9c95
# ---------------------------
@shop_bp.route("/pay/<int:order_id>")
@login_required
def pay(order_id):
<<<<<<< HEAD
    order = db.session.get(Order, order_id)
    if not order or order.user != current_user:
        flash("Unauthorized access.", "danger")
        return redirect(url_for("shop.orders"))

=======
    merchant_id = current_app.config.get('OPAY_MERCHANT_ID')
    api_key = current_app.config.get('OPAY_API_KEY')
    if not merchant_id or not api_key:
        flash("Payment temporarily disabled (missing config).", "warning")
        return redirect(url_for('shop.orders'))

    order = db.session.get(Order, order_id)
    if not order:
        flash("Order not found.", "danger")
        return redirect(url_for('shop.orders'))

    payload = {
        "merchant_id": merchant_id,
        "amount": int(order.total_amount * 100),
        "currency": "NGN",
        "callback_url": url_for('shop.verify_payment', order_id=order.id, _external=True),
        "customer_email": current_user.email
    }

    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

    try:
        response = requests.post("https://api.opay.com/payment/initiate", json=payload, headers=headers)
        data = response.json()
        if data.get("status") == "success":
            return redirect(data["payment_url"])
        flash("Payment initialization failed.", "danger")
    except Exception as e:
        flash(f"Payment error: {str(e)}", "danger")
    return redirect(url_for('shop.orders'))

# ---------------------------
# Verify Payment (Render Safe)
# ---------------------------
@shop_bp.route('/verify_payment/<int:order_id>')
@login_required
def verify_payment(order_id):
    merchant_id = current_app.config.get('OPAY_MERCHANT_ID')
    api_key = current_app.config.get('OPAY_API_KEY')
    if not merchant_id or not api_key:
        flash("Payment verification skipped (missing config).", "warning")
        return redirect(url_for('shop.orders'))

    order = db.session.get(Order, order_id)
    if not order:
        flash("Order not found.", "danger")
        return redirect(url_for('shop.orders'))

    # Mark as paid for testing
>>>>>>> 1ffaa6aa9f9629ca5a1ba5494dcad47d2fee9c95
    order.status = "Paid"
    db.session.commit()
    flash("Payment successful (mock).", "success")
    return redirect(url_for("shop.orders"))
