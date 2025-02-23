import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from dotenv import load_dotenv
from cloudinary.utils import cloudinary_url  # Importujeme cloudinary_url pro context processor

# Inicializace rozšíření
db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin(name="Admin Panel", template_mode="bootstrap4")

def create_app():
    # Načtení proměnných z .env souboru
    load_dotenv()

    # Vytvoření instance Flask aplikace s nastavením cest ke statickým souborům a šablonám
    app = Flask(__name__, static_folder="../static", template_folder="../templates")

    # Načtení konfigurace z prostředí
    app.secret_key = os.getenv('SECRET_KEY', 'nejake-tajne-heslo')
    db_user = os.getenv('DB_USER', 'root')
    db_password = os.getenv('DB_PASSWORD', '')
    db_host = os.getenv('DB_HOST', '127.0.0.1')
    db_port = os.getenv('DB_PORT', '3306')
    db_name = os.getenv('DB_NAME', 'muj_web')

    # Nastavení připojení k databázi
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Inicializace rozšíření
    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)

    # Registrace blueprintů
    from app.auth import auth_bp
    from app.main_views import main_bp
    from app.admin_routes import admin_bp

    app.register_blueprint(auth_bp)    # Routy pro autentizaci budou dostupné pod /auth/...
    app.register_blueprint(main_bp)      # Hlavní stránky pod /
    app.register_blueprint(admin_bp)     # Administrace pod /admin/...

    # Import modelů, aby se při vytváření tabulek načetly definice z models.py
    from . import models

    # Vytvoření tabulek v databázi (pokud ještě neexistují)
    with app.app_context():
        db.create_all()

    # Kontextový processor, který zpřístupní funkci cloudinary_url ve šablonách
    @app.context_processor
    def inject_cloudinary_url():
        return dict(cloudinary_url=cloudinary_url)

    return app
