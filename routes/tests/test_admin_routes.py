import pytest
from flask import Flask
from flask_login import LoginManager
from extensions import db
from models.user import User
from models.product import Product
from models.order import Order
from admin.routes import admin_bp


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config.update(
        TESTING=True,
        SECRET_KEY="test",
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)

    app.register_blueprint(admin_bp)

    with app.app_context():
        db.create_all()

        admin = User(
            username="admin",
            email="admin@test.com",
            password_hash="hashed",
            is_admin=True,
        )
        db.session.add(admin)
        db.session.commit()

        product = Product(name="Admin Product", price=5000)
        db.session.add(product)
        db.session.commit()

        order = Order(user_id=admin.id, total_amount=5000)
        db.session.add(order)
        db.session.commit()

        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def login_admin(client):
    return client.post(
        "/admin/login",
        data={"username": "admin", "password": "password"},
        follow_redirects=True,
    )


def test_admin_login_page(client):
    res = client.get("/admin/login")
    assert res.status_code == 200


def test_admin_dashboard_requires_login(client):
    res = client.get("/admin/")
    assert res.status_code in (301, 302)


def test_admin_dashboard_authenticated(client, app):
    with app.app_context():
        admin = User.query.filter_by(username="admin").first()
        admin.set_password("password")
        db.session.commit()

    login_admin(client)
    res = client.get("/admin/")
    assert res.status_code == 200
