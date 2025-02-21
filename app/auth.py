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
