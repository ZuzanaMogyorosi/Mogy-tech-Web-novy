"""
VEŘEJNÉ STRÁNKY + odesílání formuláře
"""

import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import MonthlyPromo, Cenik, SparePart
from app.email_utils import send_owner_email, send_customer_email
from app import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """
    Zobrazí domovskou stránku s nejnovější měsíční promo akcí.
    """
    promo = MonthlyPromo.query.order_by(MonthlyPromo.id.desc()).first()
    return render_template('index.html', promo=promo)

@main_bp.route('/nase-sluzby')
def services():
    """
    Zobrazí stránku s nabízenými službami.
    """
    return render_template('services.html')

@main_bp.route('/cenik')
def cenik():
    """
    Zobrazí stránku s ceníkem služeb, seskupeným podle kategorií.
    """
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
    """
    Zobrazí stránku s náhradními díly.
    """
    spare_parts = SparePart.query.all()
    return render_template('spare_parts.html', spare_parts=spare_parts)

@main_bp.route('/submit', methods=['POST'])
def submit_form():
    """
    Zpracuje odeslaný formulář, zkontroluje e-mailovou adresu a odešle e-maily
    majiteli a zákazníkovi.
    """
    full_name = request.form.get('fullName', '').strip()
    email = request.form.get('email', '').strip().lower()
    message = request.form.get('message', '')

    # Kontrola e-mailové koncovky
    if not (email.endswith('.cz') or email.endswith('.com')):
        return "Email musí končit na .cz nebo .com", 400
    if not re.match(r"[^@]+@[^@]+\.(cz|com)$", email):
        flash("Neplatný email, musí končit na .cz nebo .com")
        return redirect(url_for('main.home'))

    # Odeslání e-mailů
    send_owner_email(full_name, email, message)
    send_customer_email(full_name, email, message)

    return redirect(url_for('main.thank_you'))

@main_bp.route('/thank-you')
def thank_you():
    """
    Zobrazí stránku s poděkováním po odeslání formuláře.
    """
    return render_template('thank_you.html')

def home_redirect():
    """
    Přesměruje na domovskou stránku.
    """
    return redirect(url_for('main.home'))