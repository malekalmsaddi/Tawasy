from flask import Flask
from app.extensions import db, jwt, redis_client
from app.routes import all_blueprints
import os

from app.routes.web import web_bp

def create_app():
    app = Flask(__name__)
    app.register_blueprint(web_bp)

    # Load config
    app.config.from_object('app.config.Config')

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    redis_client.init_app(app)

    # Register Blueprints dynamically
    for bp, prefix in all_blueprints:
        app.register_blueprint(bp, url_prefix=prefix)

    # CLI command for db init
    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        print("Database initialized")

    # CLI command for creating admin user
    @app.cli.command("create-admin")
    def create_admin():
        from app.models.user import User
        email = "admin@tawasy.com"
        password = "admin123"

        if User.query.filter_by(email=email).first():
            print("Admin already exists.")
            return

        admin = User(email=email, role='admin')
        admin.set_password(password)
        db.session.add(admin)
        db.session.commit()
        print(f"Admin created: {email} / {password}")

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host='0.0.0.0')
