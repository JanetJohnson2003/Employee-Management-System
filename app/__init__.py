from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'main.login'

    # Import models **inside** the function to avoid circular import
    from .models import Admin

    # User loader for Flask-Login
    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(int(user_id))

    # Register blueprint
    from .routes import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app


