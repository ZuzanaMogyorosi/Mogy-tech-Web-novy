# ADMINISTRACE
# Tento soubor obsahuje konfiguraci Flask-Admin, který je používán pro správu dat v aplikaci.
# Pokud využíváš Flask-Admin, můžeš jej konfigurovat tady. 
# Někdo ho dává přímo do __init__.py, ale takto to máš oddělené. Můžeš sem dát i ručně psané routy pro administraci.

import os
from flask import Blueprint
from flask_admin.contrib.sqla import ModelView
try:
    from flask_admin.contrib.sqla.inline import InlineModelAdmin
except ImportError:
    from flask_admin.model import InlineFormAdmin as InlineModelAdmin
from flask_admin.form import FileUploadField
from markupsafe import Markup

import cloudinary
import cloudinary.uploader
from cloudinary.utils import cloudinary_url

from app import admin, db
from app.models import User, Cenik, MonthlyPromo, SparePart, SparePartImage
from flask_login import current_user

admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')

# Konfigurace Cloudinary – načítáme hodnoty z .env
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME'),
    api_key=os.getenv('CLOUDINARY_API_KEY'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET'),
    secure=True
)

def upload_image_to_cloudinary(file):
    """
    Nahraje soubor na Cloudinary a vrátí jeho public_id.
    Pokud objekt file nemá atribut 'stream', vrací None.
    """
    if not hasattr(file, 'stream'):
        return None
    file.stream.seek(0)
    print("Filename:", file.filename)
    data = file.read()
    print("Read data length:", len(data))
    file.seek(0)
    if len(data) == 0:
        print("Warning: File content is empty")
        return None
    result = cloudinary.uploader.upload(file)
    return result.get("public_id")

# Inline admin pro model SparePartImage
class SparePartImageInline(InlineModelAdmin):
    # Umožníme nahrání jednoho obrázku (pro každý řádek)
    form_extra_fields = {
        'public_id': FileUploadField('Nahrát obrázek', base_path='/tmp')
    }
    
    def on_model_change(self, form, model, is_created):
        file = form.data.get('public_id')
        if file and hasattr(file, 'stream'):
            uploaded_id = upload_image_to_cloudinary(file)
            if uploaded_id:
                model.public_id = uploaded_id

    def _image_preview(view, context, model, name):
        if model.public_id:
            preview_url, _ = cloudinary_url(model.public_id, width=100, height=100, crop="fill", fetch_format="auto")
            return Markup(f'<img src="{preview_url}" width="100">')
        return ""
    
    column_formatters = {'public_id': _image_preview}

# ModelView pro SparePart s inline modelem pro obrázky
class SparePartAdmin(ModelView):
    # Inicializujeme inline model s modelem SparePartImage (bez db.session)
    inline_models = (SparePartImageInline(SparePartImage),)
    
    def is_accessible(self):
        return current_user.is_authenticated

# Základní ModelView pro ostatní modely
class AdminModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated

# Registrace modelů do Flask-Admin
admin.add_view(AdminModelView(User, db.session))
admin.add_view(AdminModelView(Cenik, db.session))
admin.add_view(AdminModelView(MonthlyPromo, db.session))
admin.add_view(SparePartAdmin(SparePart, db.session))
