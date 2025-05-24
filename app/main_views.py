"""
Tento soubor obsahuje veřejné části webu – jako je domovská stránka, ceník nebo poptávkový formulář.

Formulář je vytvořen bezpečně pomocí Flask-WTF (chráněný proti zneužití).
Po odeslání se odešle potvrzovací e-mail zákazníkovi i správci webu.

Blueprint 'main' zajišťuje, že všechny tyto stránky jsou oddělené od administrace nebo přihlášení.
"""

import re
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import MonthlyPromo, Cenik, SparePart
from app.email_utils import send_owner_email, send_customer_email
from app import db

# ✳️ Doplňujeme Flask-WTF formulář a validátory
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Email


# ✳️ Definice formuláře pomocí Flask-WTF
class ContactForm(FlaskForm):
    """
    Bezpečný kontaktní formulář s CSRF ochranou a serverovou validací.
    """

    full_name = StringField("Jméno a příjmení", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired(), Email()])
    message = TextAreaField("Zpráva", validators=[DataRequired()])
    submit = SubmitField("Odeslat")


# Blueprint
main_bp = Blueprint("main", __name__)


@main_bp.route("/", methods=["GET", "POST"])
def home():
    """
    Zobrazí domovskou stránku s formulářem a promo akcí.
    Formulář je bezpečně zpracován pomocí Flask-WTF.
    """
    promo = MonthlyPromo.query.order_by(MonthlyPromo.id.desc()).first()
    form = ContactForm()

    # Když uživatel odeslal formulář
    if form.validate_on_submit():
        full_name = form.full_name.data.strip()
        email = form.email.data.strip().lower()
        message = form.message.data

        # Dodatečná validace e-mailu podle domény
        if not (email.endswith(".cz") or email.endswith(".com")):
            flash("Email musí končit na .cz nebo .com")
            return render_template("index.html", promo=promo, form=form)

        # Odeslání emailu majiteli + zákazníkovi
        send_owner_email(full_name, email, message)
        send_customer_email(full_name, email, message)

        return redirect(url_for("main.thank_you"))

    # První zobrazení stránky nebo neplatný formulář
    return render_template("index.html", promo=promo, form=form)


@main_bp.route("/nase-sluzby")
def services():
    """
    Zobrazí stránku s nabízenými službami.
    """
    return render_template("services.html")


@main_bp.route("/cenik")
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
    return render_template("priceList.html", cenik_data=grouped)


@main_bp.route("/nahradni-dily")
def nahradni_dily():
    """
    Zobrazí stránku s náhradními díly.
    """
    spare_parts = SparePart.query.all()
    return render_template("spare_parts.html", spare_parts=spare_parts)


@main_bp.route("/thank-you")
def thank_you():
    """
    Zobrazí stránku s poděkováním po odeslání formuláře.
    """
    return render_template("thank_you.html")


def home_redirect():
    """
    Přesměruje na domovskou stránku.
    """
    return redirect(url_for("main.home"))
