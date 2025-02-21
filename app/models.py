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
