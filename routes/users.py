from flask import Blueprint, render_template, request, redirect, url_for, flash, session
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
    return User.query.get(int(user_id))

# ---------------------------
# Signup
# ---------------------------
@users_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check for existing user
        if User.query.filter((User.username == username) | (User.email == email)).first():
            flash("Username or email already exists.", "danger")
            return redirect(url_for('users.signup'))

        new_user = User(username=username, email=email)
        new_user.set_password(password)

        db.session.add(new_user)
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

            # Merge session cart into DB cart
            session_cart = session.get("cart", {})
            if session_cart:
                cart = Cart.query.filter_by(user_id=user.id).first()
                if not cart:
                    cart = Cart(user_id=user.id)
                    db.session.add(cart)
                    db.session.commit()

                for pid, qty in session_cart.items():
                    pid = int(pid)
                    item = CartItem.query.filter_by(cart_id=cart.id, product_id=pid).first()
                    if item:
                        item.quantity += qty
                    else:
                        db.session.add(CartItem(cart_id=cart.id, product_id=pid, quantity=qty))

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
