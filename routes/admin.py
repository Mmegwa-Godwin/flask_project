import os
from flask import Blueprint, current_app, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from werkzeug.utils import secure_filename
from extensions import db
from models.product import Product
from models.order import Order
from models.user import User
from routes.users import load_user
from werkzeug.security import check_password_hash
from functools import wraps

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

# ---------------------------
# Admin Access Decorator
# ---------------------------
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, "is_admin", False):
            flash("Admin access required.", "danger")
            return redirect(url_for("users.login"))
        return f(*args, **kwargs)
    return decorated_function

# ---------------------------
# Admin Dashboard
# ---------------------------
@admin_bp.route("/")
@admin_required
def dashboard():
    products = Product.query.all()
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return render_template("admin/dashboard.html", products=products, orders=orders)

# ---------------------------
# Add Product
# ---------------------------
@admin_bp.route("/products/add", methods=["GET", "POST"])
@admin_required
def add_product():
    if request.method == "POST":
        name = request.form["name"]
        price = float(request.form["price"])
        image = request.files.get("image")

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            image_url = f"uploads/{filename}"
        else:
            image_url = ""

        product = Product(name=name, price=price, image_url=image_url)
        db.session.add(product)
        db.session.commit()

        flash("Product added successfully!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/add_product.html")

# ---------------------------
# Edit Product
# ---------------------------
@admin_bp.route("/products/<int:product_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == "POST":
        product.name = request.form["name"]
        product.price = float(request.form["price"])
        image = request.files.get("image")

        if image:
            filename = secure_filename(image.filename)
            image.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            product.image_url = f"uploads/{filename}"

        db.session.commit()
        flash("Product updated successfully!", "success")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/edit_product.html", product=product)

# ---------------------------
# Delete Product
# ---------------------------
@admin_bp.route("/products/<int:product_id>/delete", methods=["POST"])
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash("Product deleted successfully!", "success")
    return redirect(url_for("admin.dashboard"))

# ---------------------------
# Process Order
# ---------------------------
@admin_bp.route("/orders/<int:order_id>/process")
@admin_required
def process_order(order_id):
    order = Order.query.get_or_404(order_id)
    order.status = "Processed"
    db.session.commit()
    flash("Order processed successfully!", "success")
    return redirect(url_for("admin.dashboard"))

# ---------------------------
# Deliver Order
# ---------------------------
@admin_bp.route("/orders/<int:order_id>/deliver")
@admin_required
def deliver_order(order_id):
    order = Order.query.get_or_404(order_id)
    order.delivery_status = "Delivered"
    db.session.commit()
    flash("Order marked as delivered", "success")
    return redirect(url_for("admin.dashboard"))

# ---------------------------
# Admin Login
# ---------------------------
@admin_bp.route("/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = User.query.filter_by(username=username).first()

        if user and user.is_admin and check_password_hash(user.pwd_hash, password):
            load_user(user)
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid credentials or not an admin", "danger")
            return redirect(url_for("admin.admin_login"))

    return render_template("admin/admin_login.html")
