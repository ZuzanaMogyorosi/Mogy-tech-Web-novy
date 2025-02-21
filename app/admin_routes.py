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
