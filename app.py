from flask import Flask
from flask_login import LoginManager
from config import Config
from models import db, init_db, User  # Make sure User is imported


def create_app():
    app = Flask(__name__, static_folder='static', template_folder='templates')
    app.config.from_object(Config)

    # Initialize database
    db.init_app(app)
    init_db(app)

    # Flask-Login setup
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # --- Auto-create admin if not exists, or reset password if it doesn't match ---
    from models import User
    with app.app_context():
        admin_email = "admin@flipkart.com"
        admin_password = "Admin123"
        existing_admin = User.query.filter_by(email=admin_email, role='admin').first()
        if not existing_admin:
            admin = User(name="Flipkart Admin", email=admin_email, role='admin')
            admin.set_password(admin_password)
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin created:", admin_email, "/", admin_password)
        else:
            if not existing_admin.check_password(admin_password):
                existing_admin.set_password(admin_password)
                db.session.commit()
                print("🔄 Admin password reset to default:", admin_email)
            else:
                print("ℹ️ Admin already exists:", existing_admin.email)

    # Register blueprints
    from routes.auth import bp as auth_bp
    from routes.tickets import bp as tickets_bp
    from routes.admin import bp as admin_bp
    from routes.reports import bp as reports_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(tickets_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(reports_bp)

    # Health check route
    @app.route('/health')
    def health():
        return {'status': 'ok'}

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
