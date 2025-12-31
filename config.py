import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this-is-a-secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///shop.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

PAYSTACK_SECRET_KEY = "sk_test_xxxxx"  # your key
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
class Config:
    SECRET_KEY = '6c11068ead1ce7acd4da2f02e0bf862a0104cc0df211d7c81b1952c946405271'
    SQLALCHEMY_DATABASE_URI = "sqlite:///site.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OPay credentials
    OPAY_MERCHANT_ID = "your_merchant_id_here"
    OPAY_API_KEY = "your_api_key_here"
