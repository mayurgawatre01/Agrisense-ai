"""
FarmOS v4.0 — Main Application
Upgrades: env config, admin blueprint, weather integration,
          mandi price tracker, AI pest identifier, govt scheme finder, AI Chatbot
"""
from flask import Flask, render_template
from extensions import db, bcrypt
import os


def create_app():
    app = Flask(__name__)

    # Load .env if present
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass

    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'cropsense-secret-2024')
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB
    app.config['WEATHER_API_KEY'] = os.environ.get('WEATHER_API_KEY', '')
    app.config['DATA_GOV_API_KEY'] = os.environ.get('DATA_GOV_API_KEY', '')
    app.config['GEMINI_API_KEY'] = os.environ.get('GEMINI_API_KEY', '')
    app.config['ANTHROPIC_API_KEY'] = os.environ.get('ANTHROPIC_API_KEY', '')

    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'cropsense.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    bcrypt.init_app(app)

    os.makedirs("uploads", exist_ok=True)
    os.makedirs(os.path.join("static", "charts"), exist_ok=True)
    os.makedirs(os.path.join("static", "pest_uploads"), exist_ok=True)

    with app.app_context():
        import models  # noqa

        from auth import auth as auth_bp
        app.register_blueprint(auth_bp)

        from farmer import farmer as farmer_bp
        app.register_blueprint(farmer_bp)

        from admin import admin as admin_bp
        app.register_blueprint(admin_bp)

        from tools import tools as tools_bp
        app.register_blueprint(tools_bp)

        db.create_all()
        _create_admin()

    @app.route("/")
    def home():
        return render_template("index.html")

    return app


def _create_admin():
    from models import User
    if not User.query.filter_by(email='admin@farmos.com').first():
        hashed = bcrypt.generate_password_hash('admin123').decode('utf-8')
        admin = User(
            name='Admin',
            email='admin@farmos.com',
            password=hashed,
            role='admin',
            state='Maharashtra',
            district='Pune'
        )
        db.session.add(admin)
        db.session.commit()
        print("✅ Admin created: admin@farmos.com / admin123")


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="127.0.0.1", port=5000)