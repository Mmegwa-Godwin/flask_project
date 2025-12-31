from app import create_app
from extensions import db

# Import all models
from models.user import User
from models.product import Product
from models.cart import Cart, CartItem
from models.order import Order, OrderItem
from models.payment import Payment

app = create_app()

with app.app_context():
    db.create_all()
    print("✅ All tables created successfully!")
