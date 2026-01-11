from extensions import db
from datetime import datetime
from models.order import Order
from models.user import User

class Payment(db.Model):
    ...
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    user = db.relationship(
        'User',
        back_populates='payments'
    )
