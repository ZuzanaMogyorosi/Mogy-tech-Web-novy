from flask_login import UserMixin
from app import db
from cloudinary.utils import cloudinary_url


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


class SparePartImage(db.Model):
    __tablename__ = 'spare_part_images'
    id = db.Column(db.Integer, primary_key=True)
    spare_part_id = db.Column(db.Integer, db.ForeignKey('spare_parts.id'))
    public_id = db.Column(db.String(255), nullable=False)
    spare_part = db.relationship("SparePart", back_populates="images_rel")

class SparePart(db.Model):
    __tablename__ = 'spare_parts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.String(50), nullable=False)
    images_rel = db.relationship("SparePartImage", back_populates="spare_part", cascade="all, delete-orphan")
    
    @property
    def images(self):
        urls = []
        for img in self.images_rel:
            url, _ = cloudinary_url(img.public_id, fetch_format="auto")
            urls.append(url)
        return urls
