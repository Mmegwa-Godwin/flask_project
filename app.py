import os
from flask import Flask
from extensions import db, login_manager, csrf
from settings import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "users.login"
    csrf.init_app(app)

    # Import blueprints here AFTER extensions are initialized
    from routes.admin import admin_bp
    from routes.users import users_bp
    from routes.shop import shop_bp

    # Register blueprints

    app.register_blueprint(admin_bp)
    
    app.register_blueprint(users_bp)
    app.register_blueprint(shop_bp)

    return app


if __name__ == "__main__":
    app = create_app()
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() in ("1", "true", "yes")
    app.run(host="0.0.0.0", port=port, debug=debug)
