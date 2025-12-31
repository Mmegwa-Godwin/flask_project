from extensions import db
from datetime import datetime
from models.order import Order
from models.user import User

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='pending')  # pending, success, failed
    payment_method = db.Column(db.String(50), default='opay')
    transaction_id = db.Column(db.String(100))  # Opay transaction reference
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    order = db.relationship('Order', backref='payments')
    user = db.relationship('User', backref='payments')
