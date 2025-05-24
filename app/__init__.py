"""
Tento soubor spouští celý web.

Nastaví připojení k databázi, ochranu formulářů, přihlašování uživatelů
a propojí jednotlivé části webu (např. veřejné stránky, přihlášení, administraci).
"""

import os  # Načítá věci z prostředí, třeba proměnné z .env souboru
from typing import Dict, Callable  # Pomáhá zpřehlednit, co funkce vrací nebo přijímá

from flask import Flask  # Spouští Flask aplikaci (hlavní web)
from flask_sqlalchemy import SQLAlchemy  # Práce s databází – ukládání, načítání dat
from flask_login import LoginManager  # Přihlašování a odhlašování uživatelů
from flask_admin import Admin  # Jednoduché admin rozhraní pro správu dat
from flask_wtf.csrf import CSRFProtect  # Ochrana formulářů před zneužitím (bezpečnost)
from dotenv import load_dotenv  # Načítá citlivé údaje z .env souboru
from cloudinary.utils import (
    cloudinary_url,
)  # Vytváří odkazy na obrázky uložené v cloudu


# Inicializace rozšíření
db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin(name="Admin Panel", template_mode="bootstrap4")
csrf = CSRFProtect()  # CSRF ochrana pro formuláře---------------


def create_app() -> Flask:
    """
    Vytvoří a nakonfiguruje instanci aplikace Flask.

    Načte proměnné prostředí z .env souboru, nastaví konfiguraci aplikace,
    inicializuje rozšíření a registruje blueprinty.

    Returns:
        Flask: Instance aplikace Flask.
    """
    load_dotenv()

    # Vytvoření instance Flask aplikace s nastavením cest ke statickým souborům a šablonám
    app = Flask(__name__, static_folder="../static", template_folder="../templates")

    # Načtení konfigurace z prostředí
    app.secret_key = os.getenv("SECRET_KEY", "nejake-tajne-heslo")
    db_user = os.getenv("DB_USER", "root")
    db_password = os.getenv("DB_PASSWORD", "")
    db_host = os.getenv("DB_HOST", "127.0.0.1")
    db_port = os.getenv("DB_PORT", "3306")
    db_name = os.getenv("DB_NAME", "muj_web")

    # Nastavení připojení k databázi
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+mysqlconnector://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Inicializace rozšíření
    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    csrf.init_app(app)  # Aktivace CSRF ochrany-----------------

    # Registrace blueprintů
    from app.auth import auth_bp
    from app.main_views import main_bp
    from app.admin_routes import admin_bp

    app.register_blueprint(
        auth_bp
    )  # Routy pro autentizaci budou dostupné pod /auth/...
    app.register_blueprint(main_bp)  # Hlavní stránky pod /
    app.register_blueprint(admin_bp)  # Administrace pod /admin/...

    # Vytvoření tabulek v databázi (pokud ještě neexistují)
    with app.app_context():
        db.create_all()

    # Kontextový processor, který zpřístupní funkci cloudinary_url ve šablonách
    @app.context_processor
    def inject_cloudinary_url() -> dict:
        return {"cloudinary_url": cloudinary_url}

    return app
