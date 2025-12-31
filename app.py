from flask import Flask
from config import Config
from extensions import db, login_manager
from flask_migrate import Migrate # pyright: ignore[reportMissingModuleSource]


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'users.login'  # redirect if not logged in
    migrate = Migrate(app, db)

    # Register blueprints
    from routes.shop import shop_bp
    from routes.users import users_bp
    from routes.admin import admin_bp
    app.register_blueprint(admin_bp)
    app.register_blueprint(shop_bp)
    app.register_blueprint(users_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
