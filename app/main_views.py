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
