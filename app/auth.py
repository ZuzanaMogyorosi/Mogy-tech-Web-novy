"""
# Tento soubor obsahuje routy pro autentizaci uživatelů
# Používá Flask-WTF formulář (LoginForm), který zajišťuje CSRF ochranu a validaci
# login() zpracovává POST formulář, kontroluje uživatelské jméno a heslo
# logout() ukončí session přihlášeného uživatele
"""

from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from werkzeug.security import check_password_hash
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from app import login_manager
from app.models import User


# FlaskForm definovaný přímo v tomto souboru
class LoginForm(FlaskForm):
    username = StringField("Uživatelské jméno", validators=[DataRequired()])
    password = PasswordField("Heslo", validators=[DataRequired()])
    submit = SubmitField("Přihlásit se")


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


@login_manager.user_loader
def load_user(user_id):
    """
    Načte uživatele podle ID.
    """
    return User.query.get(int(user_id))


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """
    Zobrazí přihlašovací formulář a zpracuje přihlášení.
    Pokud jsou údeje správné, uživatel je přihlášen a přesměrován do administrace.
    Při chybných údejích se zobrazí chybová hláška.
    """
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("admin.index"))
        flash("Špatné uživatelské jméno nebo heslo", category="login")
    return render_template("login.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    """
    Odhlášení uživatele.
    """
    logout_user()
    return redirect(url_for("auth.login"))
