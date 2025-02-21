# webKUprave

## Popis

modulární architektura s využitím Application Factory Pattern a Blueprintů.

Web KUprave Tento projekt je webová aplikace pro autoservis Mogy-tech. Aplikace poskytuje různé služby jako autoservis, pneuservis, servis klimatizace, kontrolu STK a EMISE, náhradní a vrakové díly, čištění vozidel, opravy bouraných vozidel a zakázkovou výrobu výfuků.

## Instalace

Pokud již máte projekt uložený na ploše, nemusíte ho klonovat. Klonování je nutné pouze v případě, že chcete stáhnout projekt z externího zdroje, například z GitHubu. Pokud již máte všechny soubory a složky na správném místě, stačí jen ověřit, že máte správně nastavené virtuální prostředí a nainstalované všechny závislosti.

### Klonování repozitáře

```sh
git clone https://github.com/ZuzanaMogyorosi/webKUprave.git
cd webKUprave
```

### Vytvořte a aktivujte virtuální prostředí

```sh
python3 -m venv venv
source venv/bin/activate
```

Pro jistotu zkontrolujte, že jste ve virtuálním prostředí příkazem:

```sh
which python
```

Výsledek by měl být:

```
/Users/zuzanamogyorosi/Desktop/uparavujWebNaGithubu/muzesupravovatwebnagithubu/venv/bin/python
```

### Nainstalujte závislosti

```sh
pip install -r requirements.txt
```

Pokud je potřeba, upgradujte pip:

```sh
pip install --upgrade pip
```

### Spusťte aplikaci

```sh
python run.py
```

Pokud je aplikace v jiné složce, může být potřeba jiný příkaz.

## Použití

Po spuštění aplikace přejděte na http://localhost:5000 ve vašem webovém prohlížeči.

## Struktura projektu

```
webKUprave/
├── README.md
└── app/
    ├── __pycache__
    ├── __init__.py             # Inicializace aplikace
    ├── admin_routes.py         # Administrativní routy
    ├── auth.py                 # Autentizace uživatelů
    ├── email_utils.py          # Nástroje pro odesílání emailů
    ├── main_views.py           # Veřejné stránky
    ├── models.py               # Databázové modely
    ├── static                  # Statické soubory (CSS, JS, obrázky)
    ├── templates               # HTML šablony
    └── venv                    # Virtuální prostředí
run.py
```

## Soubor **init**.py

```python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from dotenv import load_dotenv

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
    app.register_blueprint(main_bp)    # Hlavní stránky pod /
    app.register_blueprint(admin_bp)   # Administrace pod /admin/...

    # Import modelů, aby se při vytváření tabulek načetly definice z models.py
    from . import models

    # Vytvoření tabulek v databázi (pokud ještě neexistují)
    with app.app_context():
        db.create_all()

    return app
```

## Soubor admin_routes.py

```python
# ADMINISTRACE
# Tento soubor obsahuje konfiguraci Flask-Admin, který je používán pro správu dat v aplikaci.
# Pokud využíváš Flask-Admin, můžeš jej konfigurovat tady.
# Někdo ho dává přímo do __init__.py, ale takto to máš oddělené. Můžeš sem dát i ručně psané routy pro administraci.

import uuid
import os
from flask import Blueprint
from flask_admin.contrib.sqla import ModelView
from flask_admin.form import FileUploadField
from markupsafe import Markup
from werkzeug.utils import secure_filename

from app import admin, db
from app.models import User, Cenik, MonthlyPromo, SparePart
from flask_login import current_user

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

UPLOAD_FOLDER = 'static/image/Spare-parts'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file):
    if file and allowed_file(file.filename):
        filename = f"{uuid.uuid4().hex}_{secure_filename(file.filename)}"
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        return filename
    return None

# Vlastní ModelView pro SparePart (nahrávání obrázků)
class SparePartAdmin(ModelView):
    form_extra_fields = {
        'image_paths': FileUploadField('Nahrát obrázek')
    }

    def on_model_change(self, form, model, is_created):
        # Při nahrání obrázku uložíme do DB cestu
        if 'image_paths' in form.data and form.data['image_paths']:
            image_file = form.data['image_paths']
            filename = save_image(image_file)
            if filename:
                model.image_paths = filename

    def _image_preview(view, context, model, name):
        if model.image_paths:
            return Markup(f'<img src="/static/image/Spare-parts/{model.image_paths}" width="100">')
        return ""

    column_list = ('id', 'name', 'price', 'image_preview')
    column_formatters = {'image_preview': _image_preview}

    def is_accessible(self):
        # Příklad kontroly přihlášeného uživatele
        return current_user.is_authenticated

# Ostatní modely mohou použít základní ModelView
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

# Registrace modelů do Flask-Admin
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Cenik, db.session))
admin.add_view(AdminModelView(MonthlyPromo, db.session))
admin.add_view(SparePartAdmin(SparePart, db.session))
```

## Soubor auth.py

```python
# Obsahuje routy a funkce týkající se autentizace. Importuje model User z models.py.

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from app import login_manager
from app.models import User
from app import db

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()

        # Kontrola uživatele a hesla
        if user and check_password_hash(user.password, password):
            login_user(user)
            # Přesměrujeme do administrace – endpoint je zde 'admin.index'
            return redirect(url_for('admin.index'))
        flash('Špatné uživatelské jméno nebo heslo')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    # Přesměrujeme na hlavní stránku – endpoint je zde 'main.home'
    return redirect(url_for('main.home'))
```

## Soubor email_utils.py

```python
# NASTAVENÍ EMAILŮ Z POPTÁVKOVÉHO FORMULÁŘE

import os
import smtplib
from email.mime.text import MIMEText
from flask import flash
from dotenv import load_dotenv

load_dotenv()

SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
SMTP_USERNAME = os.getenv('SMTP_USERNAME', '')
SMTP_PASSWORD = os.getenv('SMTP_PASSWORD', '')
EMAIL_FROM = os.getenv('EMAIL_FROM', '')
EMAIL_TO = os.getenv('EMAIL_TO', '')  # Např. mail majitele

def send_email(subject, body, recipient=None, send_to_owner=False):
    #===============================================================
    # Odešle e-mail s daným předmětem a tělem na zadanou adresu.
    # Pokud je send_to_owner=True, pošle se na EMAIL_TO (tj. majitel).
    #===============================================================
    try:
        to_addr = EMAIL_TO if send_to_owner else recipient
        if not to_addr:
            return  # Není co posílat

        msg = MIMEText(body, 'plain', 'utf-8')
        msg['Subject'] = subject
        msg['From'] = EMAIL_FROM
        msg['To'] = to_addr

        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(EMAIL_FROM, [to_addr], msg.as_string())
        server.quit()
    except smtplib.SMTPException as e:
        print(f"Chyba při odesílání emailu: {e}")
        flash("Nepodařilo se odeslat e-mail.")
```

## Soubor main_views.py

```python
# VEŘEJNÉ STRÁNKY + odesílání formuláře

import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import MonthlyPromo, Cenik, SparePart
from app.email_utils import send_email
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    promo = MonthlyPromo.query.order_by(MonthlyPromo.id.desc()).first()
    return render_template('index.html', promo=promo)

@main_bp.route('/nase-sluzby')
def services():
    return render_template('services.html')

@main_bp.route('/cenik')
def cenik():
    cenik_data = Cenik.query.order_by(Cenik.kategorie).all()
    data_dict = {}
    for row in cenik_data:
        kat = row.kategorie
        if kat not in data_dict:
            data_dict[kat] = []
        data_dict[kat].append({"nazev": row.nazev, "cena": row.cena})
    grouped = [{"kategorie": k, "polozky": v} for k, v in data_dict.items()]
    return render_template('priceList.html', cenik_data=grouped)

@main_bp.route('/nahradni-dily')
def nahradni_dily():
    spare_parts = SparePart.query.all()
    return render_template('spare_parts.html', spare_parts=spare_parts)

# ============================
# Odeslání formuláře
# ============================
@main_bp.route('/submit', methods=['POST'])
def submit_form():
    full_name = request.form.get('fullName', '').strip()
    email = request.form.get('email', '').strip().lower()
    message = request.form.get('message', '')

    # Kontrola e-mailové koncovky
    if not (email.endswith('.cz') or email.endswith('.com')):
        return "Email musí končit na .cz nebo .com", 400
    if not re.match(r"[^@]+@[^@]+\.(cz|com)$", email):
        flash("Neplatný email, musí končit na .cz nebo .com")
        return redirect(url_for('main.home'))

    # ============================
    # E-mail pro majitele
    # ============================
    subject_owner = "Nová poptávka z webu"
    email_body_owner = (
        f"Jméno: {full_name}\n"
        f"Email: {email}\n"
        f"Zpráva:\n{message}"
    )
    send_email(subject_owner, email_body_owner, send_to_owner=True)

    # ============================
    # E-mail pro zákazníka
    # ============================
    subject_customer = "Potvrzení poptávky"
    email_body_customer = (
        "Dobrý den,\n\n"
        "děkujeme za Vaši poptávku. Toto je potvrzení, že jsme ji úspěšně obdrželi.\n\n"
        f"Jméno: {full_name}\n"
        f"E-mail: {email}\n"
        f"Zpráva:\n{message}\n\n"
        "Ozveme se Vám co nejdříve.\n\n"
        "S pozdravem,\nTým Autoservis Mogy-tech"
    )
    send_email(subject_customer, email_body_customer, recipient=email)

    return redirect(url_for('main.thank_you'))

@main_bp.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

def home_redirect():
    return redirect(url_for('main.home'))
```

## Soubor models.py

```python
from flask_login import UserMixin
from app import db

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)  # V produkci by se ukládal hash

class Cenik(db.Model):
    __tablename__ = 'cenik'
    id = db.Column(db.Integer, primary_key=True)
    kategorie = db.Column(db.String(255))
    nazev = db.Column(db.String(255))
    cena = db.Column(db.String(50))

class MonthlyPromo(db.Model):
    __tablename__ = 'monthly_promo'
    id = db.Column(db.Integer, primary_key=True)
    mesic = db.Column(db.String(50))
    nadpis = db.Column(db.String(255))
    discount = db.Column(db.String(10))
    popis = db.Column(db.Text)
    phone = db.Column(db.String(50))
    address = db.Column(db.Text)
    image = db.Column(db.String(255))

class SparePart(db.Model):
    __tablename__ = 'spare_parts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(50), nullable=False)
    # Ukládáme názvy obrázků oddělené čárkou, pokud je víc obrázků
    image_paths = db.Column(db.Text, nullable=False)

    @property
    def images(self):
        """Vrátí seznam cest k obrázkům pro zobrazení na webu."""
        return [
            f"/static/image/Spare-parts/{img.strip()}"
            for img in self.image_paths.split(',')
            if img
        ]
```

## Soubor run.py

```python
from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
```

## Licence

Tento projekt je licencován pod MIT licencí.
