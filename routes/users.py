from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from extensions import db, login_manager
from models.user import User
from models.cart import Cart, CartItem

users_bp = Blueprint('users', __name__, url_prefix='/users')

# ---------------------------
# User Loader
# ---------------------------
@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))

# ---------------------------
# Signup
# ---------------------------
@users_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if User.query.filter((User.username==username)|(User.email==email)).first():
            flash("Username or email already exists.", "danger")
            return redirect(url_for('users.signup'))

        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

        flash("Account created successfully!", "success")
        return redirect(url_for('users.login'))

    return render_template('users/signup.html')

# ---------------------------
# Login
# ---------------------------
@users_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)

            # Merge session cart
            session_cart = session.get("cart", {})
            if session_cart:
                cart = user.cart
                if not cart:
                    cart = Cart(user=user)
                    db.session.add(cart)
                    db.session.commit()

                for pid_str, qty in session_cart.items():
                    pid = int(pid_str)
                    item = next((i for i in cart.items_in_cart if i.product_id==pid), None)
                    if item:
                        item.quantity += qty
                    else:
                        cart.items_in_cart.append(CartItem(product_id=pid, quantity=qty))

                db.session.commit()
                session.pop("cart")

            flash("Logged in successfully!", "success")
            return redirect(url_for('shop.index'))

        flash("Invalid credentials.", "danger")
        return redirect(url_for('users.login'))

    return render_template('users/login.html')

# ---------------------------
# Logout
# ---------------------------
@users_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully.", "info")
    return redirect(url_for('shop.index'))
