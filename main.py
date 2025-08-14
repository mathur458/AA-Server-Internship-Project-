from flask import Flask, redirect, flash, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import timedelta

db = SQLAlchemy()  # ✅ define db here

print(">>> create_app called")

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3307/flask_app'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'your-very-secret-key'
    app.permanent_session_lifetime = timedelta(minutes=10)

    db.init_app(app)
    migrate = Migrate(app, db)

    # ✅ Register blueprints after app context is ready
    from common.routes import common_bp
    from auth.routes import auth_bp
    from admin.routes import admin_bp

    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(auth_bp, url_prefix='/')
    app.register_blueprint(common_bp, url_prefix='/common')

    @app.before_request
    def auto_logout_deleted_users():
        from models import User
        user_id = session.get("user_id")
        if user_id:
            user = db.session.get(User, user_id)
            if not user or not user.is_active:
                session.clear()
                flash("You have been logged out because your account was removed.")
                return redirect(url_for('auth_bp.login'))
            
    return app
