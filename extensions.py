from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager # pyright: ignore[reportMissingImports]
from flask_wtf.csrf import CSRFProtect # type: ignore

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
