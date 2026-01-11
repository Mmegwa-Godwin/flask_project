import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session, forms, flash messages
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key")

    # Database configuration: use DATABASE_URL from Render, fallback to local SQLite
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        "sqlite:///" + os.path.join(basedir, "app.db")
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Upload folder for product images
    UPLOAD_FOLDER = os.path.join(basedir, "static/uploads")

    # Any other config you need can go here
